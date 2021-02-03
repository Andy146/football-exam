import csv
from os.path import realpath, dirname

def get_matches(teams):
    root = realpath(dirname(__file__))[:-4]
    _return = list()

    #Åpner results.csv for å hente ut alle registrerte kamper
    with open(f'{root}/data/results.csv', 'r') as file:
        reader = csv.DictReader(file)
        matches = list()
        for row in reader:
            matches.append(row)
    
    #Hele resten av funksjonen er for å gjøre om lagrede lag og poeng om til datastrukturen som er i tabell på nettsiden
    #altså finner ut av hvor mange seire, måldifferanse, antall kamper etc.
    team_results = dict()
    for team in teams['full']:
        team_results[team] = [0,0,0,0,0,0,0,0]
    for match in matches:

        #Legger til en kamp i kamp antallet til hvert av lagene
        team_results[match['lag1']][0] += 1
        team_results[match['lag2']][0] += 1

        #Sjekker hvilket lag som vant, og oppdaterer deretter stats for seier, uavgjort og tap
        if(int(match['poeng1']) > int(match['poeng2'])):
            #Lag 1 vant
            team_results[match['lag1']][1] += 1
            team_results[match['lag2']][3] += 1
        elif(int(match['poeng1']) == int(match['poeng2'])):
            #Lagene fikk uavgjort
            team_results[match['lag1']][2] += 1
            team_results[match['lag2']][2] += 1
        else:
            #Lag 2 vant
            team_results[match['lag1']][3] += 1
            team_results[match['lag2']][1] += 1
        
        #Legger til mål scoret og antall mål motstander scoret
        team_results[match['lag1']][4] += int(match['poeng1'])
        team_results[match['lag2']][4] += int(match['poeng2'])

        team_results[match['lag1']][5] += int(match['poeng2'])
        team_results[match['lag2']][5] += int(match['poeng1'])

        #Lager målforskjell
        team_results[match['lag1']][6] += int(match['poeng1']) - int(match['poeng2'])
        team_results[match['lag2']][6] += int(match['poeng2']) - int(match['poeng1'])
    
    #Legger til poengsummer, 3 poeng for seier, 1 poeng for uavgjort og 0 for tap
    for team, values in team_results.items():
        team_results[team][7] = values[1] * 3 + values[2] * 1
        _append = [team] + values
        _return.append(_append)
    
    return sort_matches(_return)

def sort_matches(l):

    #Initialiserer variabler

    #_return skal bli en sortert liste med alle lagene
    _return = list()

    #_temp_team_storage brukes for å midlertidig lagre lagenes poeng og alle dataene deres
    _temp_team_storage = dict()

    #En dictionary som inneholder alle lag sine poeng, måldifferanser og målantall
    _ranking_dict = {
        "points":[],
        "diff":[],
        "goals":[]
    }

    for li in l:
        #Legger over poeng, måldifferanse, målantall og hele lagets datasett inn i _temp_team_storage
        _temp_team_storage[li[0]] = [li[-1], li[-2], li[-4], li]

        #Legger lagets poeng, måldifferanse og målantall inn i _ranking_dict
        _ranking_dict['points'].append(li[-1])
        _ranking_dict['diff'].append(li[-2])
        _ranking_dict['goals'].append(li[-4])
    
    #Alle lags verdier blir sortert i _ranking_dict i synkende rekkefølge (mest poeng først)
    _ranking_dict['points'].sort(reverse=True)
    _ranking_dict['diff'].sort(reverse=True)
    _ranking_dict['goals'].sort(reverse=True)


    #En loop som skal gå så mange ganger som vi har lag
    for _ in l:
        for team, storage in _temp_team_storage.items():
            #Hvis den nåværende høyeste poengsummen tilhører laget
            if(storage[0] == _ranking_dict['points'][0]):
                #Hvis dette er det siste laget som må legges til i resultatet så legges det ganske enkelt til, 
                #hvis det ikke er sist må poengsummen deres være høyere enn nest høyeste poengsum (for å sjekke om det er flere med samme poengsum), 
                #hvis ikke går man videre til neste sorteringsnivå
                if(len(_ranking_dict['points'])==1 or _ranking_dict['points'][0] > _ranking_dict['points'][1]):
                    #Legger til laget i resultatlisten (som har førsteplass først, andreplass som andre element etc)
                    _return.append(storage[-1])

                    #Fjerner poengsummen og laget fra iterables slik at vi ikke får dobbelt opp med resultater
                    _ranking_dict['points'].pop(0)
                    _ranking_dict['diff'].pop(0)
                    _ranking_dict['goals'].pop(0)
                    _temp_team_storage.pop(team, None)
                    break
            #Hvis denne poengsummen ikke tilhører laget så går vi til neste lag med continue
            else:
                continue
            
            #Hvis den nåværende høyeste måldifferansen tilhører dette laget
            if(storage[1] == _ranking_dict['diff'][0]):
                #Hvis dette er det siste laget som må legges til i resultatet så legges det ganske enkelt til, 
                #hvis det ikke er sist må differansen deres være høyere enn nest høyeste differanse (for å sjekke om det er flere med samme differanse), 
                #hvis ikke går man videre til neste sorteringsnivå
                if(len(_ranking_dict['diff'])==1 or _ranking_dict['diff'][0] > _ranking_dict['diff'][1]):
                    #Legger til laget i resultatlisten (som har førsteplass først, andreplass som andre element etc)
                    _return.append(storage[-1])

                    #Fjerner verdier og lag fra iterables slik at vi ikke får dobbelt opp med resultater
                    _ranking_dict['diff'].pop(0)
                    _ranking_dict['points'].pop(0)
                    _ranking_dict['goals'].pop(0)
                    _temp_team_storage.pop(team, None)
                    break
            #Hvis denne måldifferansen ikke tilhører laget så går vi til neste lag 
            #(laget, og summen blir ikke fjernet, begge vil bli tatt hånd om ved en senere iteration)
            else:
                continue
            
            #Hvis dette målantallet tilhører dette laget
            if(storage[2] == _ranking_dict['goals'][0]):
                #Hvis dette er det siste laget som må legges til i resultatet så legges det ganske enkelt til, 
                #hvis det ikke er sist må målantall deres være høyere enn nest høyeste målantall (for å sjekke om det er flere med samme målantall), 
                #hvis ikke blir laget lagt til uansett ettersom alle sorteringsnivåer er like for flere lag
                if(len(_ranking_dict['goals'])==1 or _ranking_dict['goals'][0] > _ranking_dict['goals'][1]):
                    #Legger til laget i resultatlisten (som har førsteplass først, andreplass som andre element etc)
                    _return.append(storage[-1])

                    #Fjerner verdier og lag fra iterables slik at vi ikke får dobbelt opp med resultater
                    _ranking_dict['goals'].pop(0)
                    _ranking_dict['diff'].pop(0)
                    _ranking_dict['points'].pop(0)
                    _temp_team_storage.pop(team, None)
                    break
            #Hvis dette målantallet ikke tilhører laget så går vi til neste lag
            else:
                continue
            
            #Legger laget til i resultatet hvis alle sorteringsnivåer er like hos flere lag
            _return.append(storage[-1])
            _ranking_dict['goals'].pop(0)
            _ranking_dict['diff'].pop(0)
            _ranking_dict['points'].pop(0)
            _temp_team_storage.pop(team, None)
            break

  
    #Legger til nummerering til lagene, slik at førsteplass for nummer 1 andreplass nummer 2 etc.
    _temp = list()
    num = 1
    for r in _return:
        _temp.append([num] + r)
        num += 1
    _return = _temp


    return _return

def save_match(teams, points):
    root = realpath(dirname("__main__"))

    #Sjekker om kampen som ble lagt inn allerede er registrert
    with open(f'{root}/data/results.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if (row[0] == teams[0] and row[1] == teams[1]) or (row[0] == teams[1] and row[1] == teams[0]):
                #Returnerer en feilmelding som vises til brukeren
                return "Denne kampen finnes allerede, og kan ikke registreres på nytt"
    
    #Sjekker om brukeren har valgt samme lag to ganger
    if(teams[0]==teams[1]):
        return "Kunne ikke lagre på grunn av lagvalg, vennligst velg to forskjellige lag til å spille mot hverandre"
    
    #Hvis kampen ikke allerede er registrert så legges den til i results.csv
    with open(f'{root}/data/results.csv', 'a') as file:
        row=[teams[0], teams[1], points[0], points[1]]
        writer = csv.writer(file)
        writer.writerow(row)

    #Returnerer True for at webserveren skal forstå at kampen ble lagret uten problemer
    return True
