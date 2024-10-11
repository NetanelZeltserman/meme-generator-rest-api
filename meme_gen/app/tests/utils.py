from app.models import Meme, MemeTemplate, User
import random

def create_test_user(username='testuser', password='testpass'):
    return User.objects.create_user(username=username, password=password)

def create_meme_template(name="Test Template", image_url="http://example.com/template.jpg", 
                         default_top_text="Default Top", default_bottom_text="Default Bottom"):
    return MemeTemplate.objects.create(
        name=name,
        image_url=image_url,
        default_top_text=default_top_text,
        default_bottom_text=default_bottom_text
    )

def create_meme_templates(count):
    return [
        create_meme_template(name=f"Template {i}", image_url=f"http://example.com/template{i}.jpg")
        for i in range(1, count + 1)
    ]

def create_meme(template=None, top_text="Test Top", bottom_text="Test Bottom", user=None):
    if template is None:
        template = get_random_template()
    
    return Meme.objects.create(
        template=template,
        top_text=top_text,
        bottom_text=bottom_text,
        created_by=user
    )

def get_random_template():
    template_count = MemeTemplate.objects.count()
    if template_count > 0:
        random_index = random.randint(0, template_count - 1)
        return MemeTemplate.objects.all()[random_index]
    return None

def create_memes(count, template, user, memes_attributes=None):
    if memes_attributes is None:
        memes_attributes = {}
    
    return [
        create_meme(
            template=template,
            top_text=memes_attributes.get('top_text', f'Test Top {i}'),
            bottom_text=memes_attributes.get('bottom_text', f'Test Bottom {i}'),
            user=user,
        )
        for i in range(count)
    ]