from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import requests
from io import BytesIO
from django.core.files.base import ContentFile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='avatar.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Call the parent class's save method to ensure the object is saved first
        super().save(*args, **kwargs)
        
        # Check if the image is the default one, skip processing
        if self.image.name != 'avatar.jpg':
            try:
                # Download the image from cloud storage using the URL
                response = requests.get(self.image.url)
                img = Image.open(BytesIO(response.content))

                # Resize the image if its dimensions are larger than 300x300
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)

                    # Save the resized image to the image field
                    img_io = BytesIO()
                    img.save(img_io, format=img.format)
                    
                    # Use ContentFile to overwrite the existing image
                    self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)

            except Exception as e:
                print(f"Error processing image: {e}")

        # Save the object again to ensure changes are saved
        super().save(*args, **kwargs)




