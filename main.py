from fastapi import FastAPI, File, Form, UploadFile
import pywhatkit
import os
from typing import Optional

app = FastAPI()

@app.post("/send_whatsapp")
async def send_whatsapp(
    phone_number: str = Form(...),
    message: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    try:
        # Guardar la imagen si se proporciona
        image_path = None
        if image:
            image_path = f"temp_{image.filename}"
            with open(image_path, "wb") as img_file:
                content = await image.read()
                img_file.write(content)

        # Enviar el mensaje de WhatsApp
        if image_path:
            pywhatkit.sendwhats_image(phone_number, image_path, message)
            os.remove(image_path)  # Eliminar la imagen después de enviarla
        else:
            pywhatkit.sendwhatmsg_instantly(phone_number, message)
        
        return {"status": "success", "message": "Message sent successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)







#curl -X POST "http://127.0.0.1:8000/send_whatsapp" -F "phone_number=+56988876774" -F "message=Hola, este es un mensaje de prueba" -F "image=@C:\Users\Usuario\Desktop\api_whatsapp\imagen.png"
