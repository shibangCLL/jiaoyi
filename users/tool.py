from django.shortcuts import render

from users import models  # 从app中导入数据库


class RenderWrite(object):  # 新建一个工具类
    def render_template(request, template_name, context=None, content_type=None, status=None, using=None):
        return render(
            request=request,
            template_name=template_name,
            context=context,
            content_type=content_type,
            status=status,
            using=using
        )
