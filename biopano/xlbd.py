from pymongo import *
from django.shortcuts import HttpResponse
import bson
from datetime import *
from Bio.Blast.Applications import NcbiblastnCommandline
import os


BLAST_PATH = r'/tmp/blast'
db = MongoClient()['igemdata_new']

## unused after using blast
'''
def func(a, b):
    if a == b:
        return 1
    else:
        return -1


def NeedleWunch(s, t):
    n = len(s)
    m = len(t)
    f = [[0 for j in range(m + 1)] for i in range(n + 1)]

    for i in range(n):
        f[i + 1][0] = -2 * (i + 1)
    for j in range(m):
        f[0][j + 1] = -2 * (j + 1)

    for i in range(n):
        for j in range(m):
            f[i + 1][j + 1] = max(max(f[i + 1][j], f[i][j + 1]) - 2, f[i][j] + func(s[i], t[j]))
    return f[n][m]


def main(request):
    if request.method == 'POST':
        if 'sequence' not in request.POST.keys():
            key_list = str(request.POST.keys())
            return HttpResponse(
                "{'status':'error', 'reason':'keyword sequence is not in request.', 'keys':" + key_list + "}")
        a = request.POST['sequence'].upper()
        id_list = []
        b = []
        # what down here is ugly code!
        time_point = {}
        start_time = datetime.now()
        for u_t_r in db.u_t_r.find():
            if u_t_r['TYPE'] == 'O_T_P':
                if u_t_r['SEQUENCE_5'] is not '':
                    # id_list.append(str(u_t_r['node_id']))
                    b.append(u_t_r['SEQUENCE_5'].upper())
                if u_t_r['SEQUENCE_3'] is not '':
                    # id_list.append(str(u_t_r['node_id']))
                    b.append(u_t_r['SEQUENCE_3'].upper())
            else:
                # id_list.append(str(u_t_r['node_id']))
                b.append(u_t_r['SEQUENCE'].upper())
        time_point['datebase_reading'] = datetime.now() - start_time
        ans = -9999999999
        ansx = []
        for i in b:
            x = NeedleWunch(a, i)
            if x == ans:
                ansx += [i]
            if x > ans:
                ans = x
                ansx = [i]
        time_point['core_computing'] = datetime.now() - start_time
        result = []
        for sequence in ansx:
            for node in db.u_t_r.find({'$or': [{'SEQUENCE': sequence}, {'SEQUENCE_3': sequence}, {'SEQUENCE_5': sequence}]}):
                if str(node['node_id']) not in id_list:
                    id_list.append(str(node['node_id']))
        time_point['search_result_in_datebase'] = datetime.now() - start_time
        for each_id in id_list:
            dicts = {'_id': each_id}
            node = db.node.find_one({'_id': bson.ObjectId(each_id)})
            dicts['NAME'] = node['NAME']
            dicts['TYPE'] = node['TYPE']
            dicts['SCORE'] = ans
            result.append(dicts)
        result = str(result)
        time_point['serialize'] = datetime.now() - start_time

        time_report = '\n'.join(step + str(time_point[step]) for step in time_point.keys())
        return HttpResponse(result)
        # print ans   # mark
        #print ansx  # object list which have highest mark
    elif request.method == 'GET':
        #return HttpResponse('This is new!!!!')
        return HttpResponse("{'status':'error', 'reason':'no GET method setting'}")
'''


def blast_fasta_create():
    db = MongoClient()['igemdata_new']
    fp = r'/tmp/sequence.fasta'
    file = open(fp, 'w')
    text_list = []
    text = ''

    for utr in db.u_t_r.find({'TYPE': 'O_T_P'}):
        id = str(utr['_id'])
        sequence_5 = utr['SEQUENCE_5']
        sequence_3 = utr['SEQUENCE_3']
        id = '>' + id + '\n'
        if sequence_5:
            text = ' '.join([id, sequence_5, '\n'])
            text_list.append(text)
        '''
        if sequence_3:
            text = ' '.join([id, sequence_3, '\n'])
            text_list.append(text)
        '''
    print 'Successfully read utr sequences'

    for node in db.node.find({'TYPE': {'$in': ['Promoter', 'Gene', 'Terminator']}}):
        if 'SEQUENCE' in node.keys():
            if node['SEQUENCE']:
                id = str(node['_id'])
                id = '>' + id + '\n'
                sequence = node['SEQUENCE']
                text = ' '.join([id, sequence, '\n'])
                text_list.append(text)
    print 'Successfully read node sequences'

    for text in text_list:
        file.write(text)
    print 'Successfully write sequences'

    file.close()


def check_blast_fasta():
    if not os.path.exists(r'/tmp/blast'):
        blast_fasta_create()
        order = 'makeblastdb -in /tmp/sequence.fasta -dbtype nucl -title ustc_blast -parse_seqids -out /tmp/blast/ustc_blast'
        os.system(order)
        return True
    else:
        return True


def blast(request):
    if request.method == 'POST':
        check_blast_fasta()
        if 'sequence' not in request.POST.keys() or 'user' not in request.POST.keys():
            key_list = str(request.POST.keys())
            return HttpResponse("{'status':'error', 'reason':'keyword sequence is not in request.', 'keys':" + key_list + "}")

        # input to fasta

        '''
        fasta_path should be appended with user name such as input_beibei.fasta
        so that there wouldn't be conflict when multiuser use blast
        '''
        fasta_path = BLAST_PATH + '/input_' + request.POST['user'] +'.fasta'
        fasta_fp = open(fasta_path, 'w')
        fasta_fp.write('>query\n')
        fasta_fp.write(request.POST['sequence'] + '\n')

        cline = NcbiblastnCommandline(query=fasta_path, db='/tmp/blast/ustc_blast', strand='plus', evalue=0.00001, outfmt=11)
        stdout, stderr = cline()

        test_fp = open(BLAST_PATH + '/stdout.txt', 'w')
        test_fp.write(stdout + '\n\n' + stderr)

        return HttpResponse("result txt has been established")

    elif request.method == 'GET':
        return HttpResponse("{'function':'blast', 'status':'error', 'reason':'no GET method setting'}")