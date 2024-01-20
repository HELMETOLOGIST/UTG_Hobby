def adminame(request):
    try:
        admi = request.user.username
        return {
            "adname" : admi
        }
    except:
        return {}