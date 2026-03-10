from interface import HTML_TEMPLATE

# Check if JavaScript is in the HTML
if 'async function girisYap()' in HTML_TEMPLATE:
    print("✓ girisYap function found in HTML")
else:
    print("✗ girisYap function NOT found in HTML")

if '<script>' in HTML_TEMPLATE:
    print("✓ <script> tag found")
else:
    print("✗ <script> tag NOT found")
    
if '</script>' in HTML_TEMPLATE:
    print("✓ </script> tag found")
else:
    print("✗ </script> tag NOT found")

# Find and show the script section
start = HTML_TEMPLATE.find('<script>')
if start >= 0:
    end = HTML_TEMPLATE.find('</script>') + len('</script>')
    script_section = HTML_TEMPLATE[start:start+300]
    print("\nFirst 300 chars of <script> section:")
    print(script_section)
