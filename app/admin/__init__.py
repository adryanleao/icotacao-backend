def init_app(app):
    from app.admin import city
    city.init_app(app)

    from app.admin import company
    company.init_app(app)

    from app.admin import country
    country.init_app(app)

    from app.admin import group
    group.init_app(app)

    from app.admin import notification
    notification.init_app(app)

    from app.admin import segment
    segment.init_app(app)

    from app.admin import state
    state.init_app(app)

    from app.admin import user
    user.init_app(app)

    from app.admin import quote
    quote.init_app(app)

    from app.admin import dashboard
    dashboard.init_app(app)
