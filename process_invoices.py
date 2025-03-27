import os
from openai import AzureOpenAI
import base64
import json
from datetime import datetime
from pdf2image import convert_from_path
from io import BytesIO
from PIL import Image

def convert_pdf_to_image(pdf_path):
    """Convierte la página adecuada del PDF a imagen."""
    # Especifica la ruta a poppler si no está en el PATH
    poppler_path = r"C:\Program Files\poppler\poppler-24.08.0\Library\bin"
    
    # Convierte el PDF a imagen
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    
    # Selecciona la última página para CONSUM, primera página para el resto
    if "Consum" in pdf_path.upper():
        selected_page = images[-1]  # Última página
        print("Usando última página para factura de Consum")
    else:
        selected_page = images[0]   # Primera página
    
    # Convierte la imagen a bytes
    img_byte_arr = BytesIO()
    selected_page.save(img_byte_arr, format='JPEG', quality=95)
    img_byte_arr = img_byte_arr.getvalue()
    
    return base64.b64encode(img_byte_arr).decode('utf-8')

def process_invoice(pdf_path):
    """Procesa una factura usando GPT-4 Vision en Azure."""
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-02-15-preview",
        azure_endpoint="https://ai-tomasrenetests412294277393.openai.azure.com"
    )
    
    # Convertimos el PDF a imagen y obtenemos su base64
    base64_image = convert_pdf_to_image(pdf_path)
    
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Analiza esta factura y extrae exactamente:
                                 1. Nombre del proveedor (empresa o persona que emite la factura)
                                 2. Monto sin IVA (base imponible)
                                 3. IVA (solo el monto del IVA)
                                 4. Monto total (importe total de la factura)
                                 
                                 Responde SOLO en formato JSON con estas claves exactas:
                                 {
                                     "proveedor": "",
                                     "monto_sin_iva": 0.0,
                                     "iva": 0.0,
                                     "monto_total": 0.0
                                 }"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content

def main():
    # Cargar configuración desde config.json
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            os.environ["AZURE_OPENAI_KEY"] = config["AZURE_OPENAI_KEY"]
            os.environ["AZURE_OPENAI_ENDPOINT"] = config["AZURE_OPENAI_ENDPOINT"]
            os.environ["AZURE_OPENAI_DEPLOYMENT"] = config["AZURE_OPENAI_DEPLOYMENT"]
    except FileNotFoundError:
        print("Error: Asegúrate de crear el archivo config.json con las credenciales")
        return
    
    # Directorio de febrero
    month = "Enero"
    month_number = "01"
    invoice_dir = f"Facturas/{month_number} - {month}"
    results = []
    
    # Procesa todos los PDFs en el directorio y subdirectorios
    for root, dirs, files in os.walk(invoice_dir):
        for filename in files:
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(root, filename)
                print(f"\nProcesando: {pdf_path}")
                
                try:
                    result = process_invoice(pdf_path)
                    print("Resultado:", result)
                    
                    # Guarda el resultado
                    results.append({
                        "archivo": pdf_path,
                        "datos": result
                    })
                except Exception as e:
                    print(f"Error procesando {pdf_path}: {str(e)}")
    
    # Guarda todos los resultados en la carpeta Resultados
    os.makedirs("Resultados", exist_ok=True)
    output_file = f"Resultados/resultados_{month}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nTodos los resultados guardados en: {output_file}")

if __name__ == "__main__":
    main() 