import base64

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def main():
    image_path = "nutrient_intake.png"
    encoded_image = get_base64_encoded_image(image_path)
    
    html_str = f'''
    <html>
    <body>
    <img src="data:image/png;base64,{encoded_image}" alt="Nutrient Intake Graph">
    </body>
    </html>
    '''
    
    with open("dashboard.html", "w") as html_file:
        html_file.write(html_str)

if __name__ == "__main__":
    main()
