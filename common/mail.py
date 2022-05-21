from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail


def send(subject, title, content, recipient_list, from_mail=settings.DEFAULT_FROM_EMAIL):
    res = send_mail(
        subject=subject,
        message='JOHNSON',
        html_message="""<div style="width: 630px;margin: 0 auto;background: #FFFFFF;box-shadow: 0px 3px 13px 0px rgba(71, 120, 199, 0.2);border-radius: 4px;">
    <div style="height: 4px;background: #4778C7;border-radius: 4px;"></div>
    <div style="padding: 0 40px;">
        <div style="font-size: 16px;color: #163366;line-height: 32px;margin: 40px 0 10px 0;">{TITLE}:</div>
        <div style="font-size: 14px;color: #7586A6;line-height: 30px;margin-bottom: 54px;">
           {CONTENT}
        </div>
        <div style="font-size: 13px;color: #9eafce;line-height: 30px;">
            这封电子邮件由系统自动生成，请勿回复。如果您需要额外帮助，请联系系统管理员。
        </div>
    </div>
    <div style="height: 35px;line-height: 35px;background: #F2F7FF;border-radius: 4px;padding: 0 40px;">
        <span style="float: left;font-size: 12px;color: #7586A6;">©{YEAR} J0hNs0N</span>
        <span style="float: right;">
            <a href="https://gitee.com/J0hNs0N/FlawPlatform" target="_blank"
               style="float: left;margin-right: 9px;margin-top: 3px;" rel="noopener">
                <img src="https://gitee.com/assets/favicon.ico" style="height: 16px;width: 16px;" alt="Gitee 码云">
            </a>
            <a href="https://forum.butian.net/people/4602/community" target="_blank"
               style="float: left;margin-right: 9px;margin-top: 3px;" rel="noopener">
                <img src="https://forum.butian.net/ico.png" style="height: 20px;width: 20px;" alt="奇安信攻防社区">
            </a>
            <a href="https://space.bilibili.com/274407612" target="_blank"
               style="float: left;margin-right: 9px;margin-top: 2px;" rel="noopener">
                <img src="https://www.bilibili.com/favicon.ico?v=1" style="height: 16px;width: 16px;" alt="哔哩哔哩">
            </a>
        </span>
    </div>
</div>""".format(YEAR=datetime.now().year, TITLE=title, CONTENT=content),
        from_email=from_mail,
        recipient_list=recipient_list,
    )
