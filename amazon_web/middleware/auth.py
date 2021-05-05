from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin 

class authMiddleware(MiddlewareMixin): 
    def process_response(self, request, response): 
        # 非ログイン時: ログイン画面にリダイレクト
        if not request.user.is_authenticated:
            if request.path not in ['/login/','/account/signup/']: 
                # return HttpResponseRedirect('/data_view/manual')
                return HttpResponseRedirect('/login/')
        # ログイン時: 初期画面にリダイレクト
        else:
             if request.path in ['','/','/login/']: 
                return HttpResponseRedirect('/data_view/manual')
        return response
