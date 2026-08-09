import os, re

base_dir = r'V:\__Purecomp'
pages_dir = os.path.join(base_dir, 'pages')

# Fix about-us.html: href="/get-help-now/contact" -> href="get-help-now.html"
p = os.path.join(pages_dir, 'about-us.html')
if os.path.exists(p):
    h = open(p, encoding='utf-8').read()
    h = h.replace('href="/get-help-now/contact"', 'href="get-help-now.html"')
    open(p, 'w', encoding='utf-8').write(h)
    print('Fixed about-us.html contact link')

# Fix referral-program.html: href="/get-help-now/contact/get-help" -> href="get-help-now.html"
p = os.path.join(pages_dir, 'referral-program.html')
if os.path.exists(p):
    h = open(p, encoding='utf-8').read()
    h = h.replace('href="/get-help-now/contact/get-help"', 'href="get-help-now.html"')
    h = h.replace('href="/privacy"', 'href="privacyterms-privacy-policy.html"')
    h = h.replace('href="/terms"', 'href="privacyterms-disclaimers.html"')
    open(p, 'w', encoding='utf-8').write(h)
    print('Fixed referral-program.html links')

print('Additional link fixes applied.')
