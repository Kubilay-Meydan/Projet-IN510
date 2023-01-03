#dependencies
import argparse

#input parser
parser = argparse.ArgumentParser(description='Permet de parser les arguments')
parser.add_argument('Fonction', metavar='Fonction', type=str,
                help='fonction a executer (se referer au README)')
parser.add_argument('Machine1', metavar='Machine1', type=str,
                help='nom ou chemin du Fichier .txt du code de la machine 1')
parser.add_argument('Mot', metavar='Mot', type=str,
                help='mot (alphabet 0,1) ')
parser.add_argument('--Machine2', metavar='Machine2', type=str, required= False,
                help='nom ou chemin du Fichier .txt du code de la machine 2 (optionel)')                 
args = parser.parse_args()

#Question 1

class MT:
    def __init__(self, etat_courant, etat_bandes, position_tete_lecture, etat_final, transitions, link):
        self.etat_courant = etat_courant
        self.etat_bandes = etat_bandes
        self.position_tete_lecture = position_tete_lecture
        self.etat_final = etat_final
        self.transitions = transitions
        self.link = link

def lirefichier(fichiertxt, mot):
    etat_bandes = []
    position_tete_lecture = []
    etat_courant = []
    etat_final = []
    transitions = []
    link = []
    p1 = MT(etat_courant, etat_bandes, position_tete_lecture,
            etat_final, transitions, link)

    # lis le fichier et stoque les lignes raw dans lines
    with open(fichiertxt) as file:
        lines = []
        for line in file:
            line = line.splitlines()
            lines.append(line)
    # on retire les commentaires et les lignes blanches
    rm = []
    for i in lines:
        if str(i).startswith("['/") or i == ['']:
            rm.append(i)
    for i in rm:
        lines.remove(i)

    # on met l'etat init comme l'etat courant
    for i in lines:
        if str(i).startswith("['init"):
            parsed = str(i).split(':')
            etat_courant.append(parsed[1][1:-2])
        if str(i).startswith("['accept"):
            parsed = str(i).split(':')
            etat_final.append(parsed[1][1:-2])
        if str(i).startswith("['link"):
            parsed = str(i).split(':')
            link.append((str(parsed[1][1:-2])).split(','))

    # on retire les names, inits et accepts...
    rm = []
    for i in lines:
        if str(i).startswith("['name") or str(i).startswith("['init") or str(i).startswith("['accept") or str(i).startswith("['link"):
            rm.append(i)
    for i in rm:
        lines.remove(i)

    global Nombre_bandes
    # calculateur du nombre de bandes: on compte le nombre d'elements de la ligne 1 separes par des ","
    Nombre_bandes = (len(str(lines[0]).split(','))) - 1

    # met le bon nombre de sous listes dans etat_bandes et met les tetes de lectures en postion 0.

    for i in range(Nombre_bandes):
        etat_bandes.append([])

    for i in range(Nombre_bandes):
        # car caractère '_' au début de chaque bande
        position_tete_lecture.append([1])

    # on met le mot dans la bande 1
    # permet d'accéder aux indices du mot de manière
    mot_sep = [str(a) for a in str(mot)]
    etat_bandes[0] = mot_sep
    L_inter = ['_' for i in range((len(mot_sep)+2))]
    etat_bandes[0].append('_')
    etat_bandes[0].insert(0, '_')
    for i in range(1, Nombre_bandes):
        etat_bandes[i] = L_inter
    return (p1)

def charge_transitions(fichiertxt, mot):
    p1 = lirefichier(fichiertxt, mot)
    # lis le fichier et stoque les lignes raw dans lines
    with open(fichiertxt) as file:
        lines = []
        for line in file:
            line = line.splitlines()
            lines.append(line)

    # on retire les commentaires, les lignes blanches et les options supplementaires
    rm = []
    for i in lines:
        if str(i).startswith("['/") or i == [''] or i == [' '] or str(i).startswith("['name") or str(i).startswith("['init") or str(i).startswith("['accept") or str(i).startswith("['link"):
            rm.append(i)
    for i in rm:
        lines.remove(i)
    # recuprere les etats dans les lignes du fichier txt
    etats = []
    for i in lines:
        parsed = str(i).split(',')
        etats.append(parsed[0][2:])

    transitions = {}

    # cree un dico transtion avec chaque etat possible
    for i in etats:
        if i not in transitions:
            transitions[i] = []

    # met les transitions "lues" dans le dico transition.
    for i in range(len(lines)):
        if i % 2 == 0:
            for y in transitions.keys():
                parsed = str(lines[i])[2:-2].split(',')
                if parsed[0] == y:
                    transitions[y].append([])
                if parsed[0] == y:
                    for x in range(Nombre_bandes):
                        k = 0
                        while len(transitions[y][k]) > Nombre_bandes:
                            k += 1
                        transitions[y][k].append(parsed[x+1])
                        if len(transitions[y][k]) == Nombre_bandes:
                            transitions[y][k].append(
                                str(lines[i+1])[2:-2].split(','))
    p1.transitions.append(transitions)
    return p1


#Question 2

def premiere_etape(p1, mot):
    trouve = 0
    id = 0
    trs_utilises = []
    print("etats des bandes:")
    for bandes in p1.etat_bandes:
        print(str(bandes)+'\n')
    if p1.etat_courant[0] != 'reject':
        '''
        idlink = 0
        if p1.link != []:
            for links in p1.link:
                # print(links[0])
                if p1.etat_courant[0] == links[0]:
                    for u in range(Nombre_bandes):
                        # print(links[Nombre_bandes+u],p1.etat_bandes[u][p1.position_tete_lecture[u][0]],Nombre_bandes)
                        if p1.etat_bandes[u][p1.position_tete_lecture[u][0]] == links[Nombre_bandes+u]:
                            idlink += 1
                    if idlink == Nombre_bandes:
                        print('link detecte, on execute la machine:',
                              links[Nombre_bandes+1])
                        old_nombre_bande = Nombre_bandes
                        if (run_machine(links[Nombre_bandes+1], mot)) == True:
                            p1.etat_courant[0] = (links[old_nombre_bande+2])
                            return p1
        '''
        for trs in p1.transitions[0][p1.etat_courant[0]]:
            if id != Nombre_bandes:
                id = 0
                # pour chaque trantion trs dans transition, on va checher si le contenu de etat bande a l'indice des tetes, correstpond a la partie lue des transitions
                for u in range(Nombre_bandes):
                    if trs[u] == p1.etat_bandes[u][p1.position_tete_lecture[u][0]] and id != Nombre_bandes:
                        # print(trs[u], p1.etat_bandes[u][p1.position_tete_lecture[u][0]], "meme")
                        id += 1
                    # on verifie qu'il y a autant de correspondances que de tetes de lectures (ou nb de bandes)
                if id == Nombre_bandes:
                    trs_utilises.append([p1.etat_courant, trs])
                    if trs[Nombre_bandes][0] == p1.etat_final[0]:
                        p1.etat_courant[0] = p1.etat_final[0]
                        return p1
                    trouve += 1
                    print('transition effectuee:',trs)
                    # on remplace l'etat courant vers l'etat destination
                    p1.etat_courant[0] = trs[Nombre_bandes][0]
                    # faire la maj des bandes et des psotitions des marqueurs
                    for u in range(Nombre_bandes):
                        p1.etat_bandes[u][p1.position_tete_lecture[u][0]] = trs[Nombre_bandes][u+1]
                        #print(trs[Nombre_bandes][u+1], u+1)
                        #print(p1.position_tete_lecture)
                    for u in range(Nombre_bandes):
                        if trs[Nombre_bandes][u+Nombre_bandes+1] == '>':
                            p1.position_tete_lecture[u][0] += 1
                            if p1.position_tete_lecture[u][0] == len(p1.etat_bandes[u])-1:
                                p1.etat_bandes[u].append('_')
                        if trs[Nombre_bandes][u+Nombre_bandes+1] == '<':
                            p1.position_tete_lecture[u][0] -= 1
                            if p1.position_tete_lecture[u][0] == 0:
                                p1.etat_bandes[u].insert(0, '_')
                                p1.position_tete_lecture[u][0] += 1
    if trouve == 0:
        #si on ne trouve pas de transitions possibles
        p1.etat_courant[0] = 'reject'
        return p1

    return p1


#Question 3,4

def run_machine(fichiertxt, mot):
    b = charge_transitions(fichiertxt, mot)
    F = b.etat_final
    c = premiere_etape(b, mot).etat_courant
    while c[0] != F[0]:
        c = premiere_etape(b, mot).etat_courant
        print(c, 'etat courant')
        if c[0] == 'reject':
            print("le mot est rejette")
            return False
    print('\n'+"bandes de la machine", fichiertxt, "sont :", '\n', b.etat_bandes,'\n',
          'les tetes de lectures sont a:', '\n', b.position_tete_lecture)
    print()
    return True


#Question 5:
# voir dossier


#Question 5:
# voir dossier


#Question 6:

def linker(machine1, machine2):
    m1 = charge_transitions(machine1, '')
    m2 = charge_transitions(machine2, '')
    trs_m1 = (m1.transitions[0])
    I_m1 = (m1.etat_courant[0])
    F_m1 = (m1.etat_final[0])
    L_m1 = (m1.link)
    trs_m2 = (m2.transitions[0])
    I_m2 = m2.etat_courant[0]
    F_m2 = m2.etat_final[0]
    if L_m1 == []:
        print("Il n'y a pas de link dans la machine 1 vers la machine 2")
        return False 
    with open('linker.txt', 'w') as f:
        init = str("init: " + I_m1 + '\n')
        accept = str("accept: " + F_m1 + '\n')
        f.write(init)
        f.write(accept)
        f.write('\n''\n')
        # copie du code de la machine 1 vers un fichier 'linker.txt'

        for etat in trs_m1.keys():
            # formating des valeurs
            for values in trs_m1[etat]:
                lct = ''
                for elem in range(0, Nombre_bandes):
                    l = values[elem]
                    lct += ','+str(l)
                f.write(etat+','+lct[1:]+'\n')
                reste = ''
                for u in values[Nombre_bandes]:
                    reste += str(u)+','
                f.write(reste[:-1]+'\n')
                f.write('\n')
        nbdelink = 0

        for links in L_m1:
            f.write('\n'+'//link')
            f.write('\n')
            lecture = ''
            for elem in range(1, Nombre_bandes+1):
                l = links[elem]
                lecture += ','+str(l)
            move = ',-'*Nombre_bandes
            f.write(links[0]+lecture + '\n')
            f.write('Linked_'+str(nbdelink)+'_'+I_m2+lecture+move+'\n'+'\n')

            for etat in trs_m2.keys():
                # formating des valeurs
                for values in trs_m2[etat]:
                    lc = ''
                    for elem in range(Nombre_bandes):
                        l = values[elem]
                        lc += ','+str(l)

                    f.write('Linked_'+str(nbdelink)+'_'+etat+','+lc[1:]+'\n')
                    reste = ''
                    for u in values[Nombre_bandes]:
                        # on remplace l'etat final de la machine 2 par l'etat destination de la trs link
                        if u == F_m2:
                            u = links[-1]
                        reste += str(u)+','
                    if str(reste).startswith(str(links[-1])):
                        f.write(reste[:-1]+'\n')
                        f.write('\n')
                    else:
                        f.write('Linked_'+str(nbdelink)+'_'+reste[:-1]+'\n')
                        f.write('\n')
            nbdelink += 1
            print('\n'+"Fichier linker.txt combinant"+'\n'+str(machine1)+'\n'+ "et"+'\n'+ str(machine2) + '\n'+ "a ete cree")


#Question 7, 8:
# voir dossier


#bonus question10:
def dead_code_remover(fichiertxt,mot):
    mt = charge_transitions(fichiertxt,mot)
    trs = mt.transitions[0]
    trs_lues = []
    for a in (trs.keys()):
        trs_lues.append(a)
    transitions = []
    trs_atteintes = []

    for keys in trs_lues:
        transitions.append(trs[keys])
    for elem in transitions:
        for h in elem:
            if h[Nombre_bandes][0] not in trs_atteintes:
                trs_atteintes.append(str(h[Nombre_bandes][0]))
    dead_trans = []
    for elem in trs_lues:
        if elem not in trs_atteintes:
            dead_trans.append(elem)
    with open('_no_dead_'+ fichiertxt, 'w') as f:
        init = str("init: " + mt.etat_courant[0] + '\n')
        accept = str("accept: " + mt.etat_final[0] + '\n')
        f.write(init)
        f.write(accept)
        f.write('\n''\n')
        for etat in trs.keys():
            if etat not in dead_trans:
                # formating des valeurs
                for values in trs[etat]:
                    lct = ''
                    for elem in range(0, Nombre_bandes):
                        l = values[elem]
                        lct += ','+str(l)
                    f.write(etat+','+lct[1:]+'\n')
                    reste = ''
                    for u in values[Nombre_bandes]:
                        reste += str(u)+','
                    f.write(reste[:-1]+'\n')
                    f.write('\n')

            
    print(fichiertxt +'_no_dead.txt','a ete cree, les transitions des etats morts:'+'\n'+str(dead_trans)+ '\n' + 'ont ete enleves')
    return True


#args

possible_values = ['charge_transitions','premiere_etape','run_machine','linker','dead']
if args.Fonction == 'charge_transitions':
    mach = charge_transitions(args.Machine1,args.Mot)
    print('\n'+"etat courant (initial):",mach.etat_courant,'\n')
    print("bandes:",mach.etat_bandes,'\n')
    print("etat final:",mach.etat_final, '\n')
    print("dico des transitions:",mach.transitions,'\n')
    print("les links, s'il y en a:",mach.link,'\n')

if args.Fonction == 'premiere_etape':
    mach = premiere_etape(charge_transitions(args.Machine1,args.Mot),args.Mot)
    print('\n'+"etat courant:",mach.etat_courant,'\n')
    print("bandes:",mach.etat_bandes,'\n')
    print("positions des tetes:", mach.position_tete_lecture)

if args.Fonction == 'run_machine':
    mach = run_machine(args.Machine1,args.Mot)
    print(mach)

if args.Fonction == 'linker':
    if args.Machine2 == None:
        print('il faut une seconde machine')
    else:
        linker(args.Machine1, args.Machine2)

if args.Fonction == 'dead':
    dead_code_remover(args.Machine1, args.Mot)

if args.Fonction not in possible_values:
    print('Fonction non reconnue')
