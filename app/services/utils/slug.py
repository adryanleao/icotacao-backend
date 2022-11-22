from slugify import slugify
from sqlalchemy import func


def create_slug(classe, name):
    query = classe.query \
        .with_entities(classe.id, classe.slug) \
        .filter(classe.name == name) \
        .order_by(func.length(classe.slug).desc(), classe.slug.desc()) \
        .filter(classe.created_at == None) \
        .first()

    if query is not None:
        last_slug = query.slug
        last_slug_number = last_slug.split('-')[-1]
        try:
            slug_number = int(last_slug_number) + 1
        except:
            slug_number = 2
        slug = '{}-{}'.format(slugify(name), slug_number)
    else:
        slug = slugify(name)

    query_verify = classe.query.with_entities(classe.id, classe.slug).filter(classe.slug == slug).first()
    if query_verify is not None:
        slug = '{}-{}'.format(slug, 1)

    return slug


def create_simple_slug(name):
    slug = slugify(name)
    return slug
