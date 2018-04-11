from django.db import models

# import smtplib
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

from django.template.loader import render_to_string
from django.conf import settings


from product.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50, blank=True)

    delivery_country = models.CharField(max_length=50)
    delivery_state = models.CharField(max_length=50)
    delivery_city = models.CharField(max_length=50)
    delivery_address = models.CharField(max_length=150)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return 'Order #{}'.format(self.id)

    @property
    def total_cost(self):
        return sum(item.cost for item in self.items.all())

    @property
    def currency(self):
        return self.items.first().currency

    def send_mail(self, copy_to_manager=False, request=None, **kwargs):
        addr_from = settings.EMAIL_FROM
        addr_to = [kwargs.get('email')]
        if copy_to_manager:
            addr_to.extend(settings.EMAIL_MANAGER_ADDRS)
        # passwd = settings.EMAIL_PASSWORD
        # Prepare context for rendering templates for mails
        kwargs['base_url'] = request.build_absolute_uri('/')[:-1]
        kwargs['order'] = self

        # msg = MIMEMultipart('alternative')
        # msg['Subject'] = f'Замовлення в магазині "{settings.PROJECT_NAME}"'
        # msg['From'] = addr_from
        # msg['To'] = addr_to
        html = render_to_string('order/email.html', context=kwargs, request=request)
        text = render_to_string('order/plain_text.html', context=kwargs)
        # part1 = MIMEText(text, 'plain')
        # part2 = MIMEText(html, 'html')
        # msg.attach(part1)
        # msg.attach(part2)
        subject = f'Замовлення в магазині "{settings.PROJECT_NAME}"'

        msg = EmailMultiAlternatives(subject, text, addr_from, addr_to)
        msg.attach_alternative(html, "text/html")
        msg.send()

        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.ehlo()
        # server.starttls()
        # server.login(addr_from, passwd)
        # server.sendmail(addr_from, addr_to, msg.as_string())
        # server.quit()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')

    price = models.DecimalField(decimal_places=2, max_digits=8)
    currency = models.CharField(max_length=3)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return 'Order item #{}'.format(self.id)

    @property
    def cost(self):
        return self.price * self.quantity
