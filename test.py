import simpletable

test_data = ['john','jack','joseph','jessy','jenny','john','jack','joseph','jessy','jenny','john','jack','joseph','jessy','jenny','john','jack','joseph','jessy','jenny']
formatted_data = simpletable.fit_data_to_columns(test_data, 1)
table = simpletable.SimpleTable(formatted_data)
html_page = simpletable.HTMLPage(table)
html_page.save("test_page.html")