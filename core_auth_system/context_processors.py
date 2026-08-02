def welcome_banner(request):
    accepted = request.COOKIES.get('site_offer_accepted') == 'true'
    show_banner = not accepted and not request.session.get('banner_shown', False)

    if show_banner:
        request.session['banner_shown'] = True

    return {'welcome_banner': show_banner}