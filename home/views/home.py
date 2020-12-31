""" Home views. """
# Django
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from io import BytesIO
from django.template.loader import get_template, render_to_string
from django.db import transaction
from xhtml2pdf import pisa
import os
from django.contrib.gis.geoip2 import GeoIP2

def home(request):
    """ Load home view """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    g = GeoIP2()
    print('==================')
    print(g.city('mega.nz'))
    # print(g.country(ip))
    print('==================')
    
    context = {}
    return render(request, request.session.get('lang', 'en')+'/home.html', context)

def what_we_do(request):
    """ Renders view considering the language in the session """
    context = {}
    return render(request, request.session.get('lang', 'en')+'/what-we-do.html', context)

def research_and_reports(request):
    """ Renders view considering the language in the session """
    context = {}
    return render(request, request.session.get('lang', 'en')+'/research-and-reports.html', context)

def stories(request):
    """ Renders view considering the language in the session """
    context = {}
    return render(request, request.session.get('lang', 'en')+'/stories.html', context)

def take_action(request):
    """ Renders view considering the language in the session """
    context = {}
    return render(request, request.session.get('lang', 'en')+'/take-action.html', context)

def press_centre(request):
    """ Renders view considering the language in the session """
    context = {}
    return render(request, request.session.get('lang', 'en')+'/press-centre.html', context)

def about_unicef(request):
    """ Renders view considering the language in the session """
    context = {}
    return render(request, request.session.get('lang', 'en')+'/about.html', context)

def where_we_work(request):
    """ Renders view considering the language in the session """
    context = {}
    return render(request, request.session.get('lang', 'en')+'/where-we-work.html', context)

def careers(request):
    """ Renders view considering the language in the session """
    context = {}
    return render(request, request.session.get('lang', 'en')+'/careers.html', context)

def donate(request):
    """ Renders view considering the language in the session """
    # print('===========HERE WE GOOOO===========')
    # twocheckout.Api.auth_credentials({
    #     'private_key': 'C45E1E7A-5AC8-4F56-8F52-76878BB9664E',
    #     'seller_id': '250599272465',
    #     'mode': 'sandbox'
    # })

    # params = {
    #     'merchantOrderId': '123',
    #     'token': 'ODAxZjUzMDEtOWU0MC00NzA3LWFmMDctYmY1NTQ3MDhmZDFh',
    #     'currency': 'USD',
    #     'total': '1.00',
    #     'billingAddr': {
    #         'name': 'Testing Tester',
    #         'addrLine1': '123 Test St',
    #         'city': 'Columbus',
    #         'state': 'OH',
    #         'zipCode': '43123',
    #         'country': 'USA',
    #         'email': 'cchristenson@2co.com',
    #         'phoneNumber': '555-555-5555'
    #     }
    # }
    # try:
    #     result = twocheckout.Charge.authorize(params)
    #     print(result.responseCode)
    # except twocheckout.TwocheckoutError as error:
    #     print(error.msg)
    # print('=======================================')
    context = {}
    return render(request, 'en/donate.html', context)

def send_email(request):
    """ Generate pdf to atttach to donation email """
   
    context = {
        'name': 'Anibal :D'
    }
    # pdf = render_to_pdf('en/pdfs/donation.html', context)
    # return HttpResponse(pdf, content_type='application/pdf')

    # return render(request, 'en/pdfs/donation.html', context)
    generate_pdf('en/pdfs/donation.html', context)
    
    # Send response email after a donation with generated pdf
    with transaction.atomic():
        message = render_to_string('en/emails/donation.html', context, request=request)
        subject = 'Thank you for your help!'
        email_address = 'anibal@sappitotech.com'
        email = EmailMessage(subject, message, 'cardozo.anibal@gmail.com', [email_address])
        email.content_subtype = 'html'
        file = open('media/test.pdf', 'r')
        email.attach('test.pdf',file.read(),'text/plain')
        email.send()

    return HttpResponse('Sent')

def convertHtmlToPdf(self,sourceHtml, outputFilename):
    """
        Open output file for writing (truncated binary) and
        converts HTML code into pdf file format

    :param sourceHtml: The html source to be converted to pdf
    :param outputFilename: Name of the output file as pdf
    :return: Error if pdf not generated successfully
    """
    resultFile = open(outputFilename, "w+b")
    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(sourceHtml, dest=resultFile)
    # close output file
    resultFile.close()
    # return True on success and False on errors
    return pisaStatus.err 

def generate_pdf(template_src, context_dict={}):
    """ Function to render a django template into a pdf in a static location """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)
    file = open('media/test.pdf', "w+b")
    pisa_status = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    file.close()

    return True

def render_to_pdf(template_src, context_dict={}):
    """Function to render a django template into a pdf """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

def set_lang(request, lang):
    print('----SET SESSION LANG---')
    print(lang)
    print('-----------------------')
    request.session['lang'] = lang
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))