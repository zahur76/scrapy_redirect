import js2py
import html

js = """ function escramble_758(){ var zahur = [];
        var l=new Array();
        l[0]='>';l[1]='a';l[2]='/';l[3]='<';l[4]='|97';l[5]='|122';l[6]='|46';l[7]='|111';l[8]='|99';l[9]='|46';l[10]='|115';l[11]='|110';l[12]='|103';l[13]='|105';l[14]='|115';l[15]='|110';l[16]='|111';l[17]='|105';l[18]='|116';l[19]='|99';l[20]='|97';l[21]='|64';l[22]='|111';l[23]='|102';l[24]='|110';l[25]='|105';l[26]='>';l[27]='"';l[28]='|97';l[29]='|122';l[30]='|46';l[31]='|111';l[32]='|99';l[33]='|46';l[34]='|115';l[35]='|110';l[36]='|103';l[37]='|105';l[38]='|115';l[39]='|110';l[40]='|111';l[41]='|105';l[42]='|116';l[43]='|99';l[44]='|97';l[45]='|64';l[46]='|111';l[47]='|102';l[48]='|110';l[49]='|105';l[50]=':';l[51]='o';l[52]='t';l[53]='l';l[54]='i';l[55]='a';l[56]='m';l[57]='"';l[58]='=';l[59]='f';l[60]='e';l[61]='r';l[62]='h';l[63]=' ';l[64]='a';l[65]='<';
        for (var i = l.length-1; i >= 0; i=i-1){
        if (l[i].substring(0, 1) == '|') zahur.push("&#"+unescape(l[i].substring(1))+";");
        else zahur.push(unescape(l[i]));}

        return zahur } escramble_758() """


def converter(js):

    # print(js)

    result = str(js2py.eval_js(js))

    # print(result)

    email = ''

    for i in range(0, len(result)):
        if result[i] == '>':
            break
        if result[i]=='&':
            email += (html.unescape(result[i:i+5].replace(';', '')))

    return email


# converter(js)