import subprocess



#def printer():
#    pdf = open("./pdfs/{}.pdf".format('h.melnyczuk@gmail.com’), r)
#    lpr =  subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
#    print(lpr)
#    lpr.stdin.write(pdf)

def run(_string):
    subprocess.run(["/usr/bin/lpr", _string])

run('pdfs/h.melnyczuk@gmail.com.pdf')
