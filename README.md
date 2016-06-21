# ISOskaba 2.0
Sähköinen ISOpistejärjestelmä AYY:n ISOille

## Asennus

*TODO*

## Projektinhallintatyökalut ja menetelmät

- **Trello** - pitää kirjaa taskeista ja backlogista
  * Trello-linkki -> https://trello.com/invite/isoskaba20/980fcc02354bb6aef511ced44e95b3c2 
- **Git** - versionhallinta
- **GitHub** - repositorionhallinta, issuet
- **Scrum** - sovellettu versio Scrumista projektin hallintaan

## Lyhyesti kehityskulusta

- **Srumissa** kehitys tapahtuu sprinteissä. Pidetään 2:n viikon sprintit, joiden alussa päätetään mitä taskeja kukin tekee. Sprintin lopuksi käydään läpi lopputulos ja pohditaan mitä meni hyvin ja missä on kehitettävää. Tämän jälkeen aloitetaan seuraava sprintti. Sprintin aikana pidetään muut ajan tasalla omista tekemisistä Telegramin välityksellä sekä Trellon avulla. Jos omassa taskissa tulee esteitä, näistä kerrotaan muulle kehitystiimille niin voidaan yhdessä ratkoa. 
- **Trellossa** taskin elinkaari on:
  * Product backlog, näistä päätetään sprintin alussa tehtävät taskit
  * Sprint backlog, käynnissä olevan sprintin taskit
  * Started, task aloitettu
  * Tests made, testit taskille kirjoitettu
  * Ready, valmiina tarkastettavaksi. Tässä vaiheessa tehdään GitHubissa pull request.
  * Complete, pull request hyväksytty eli taskissa tehdyt asiat ovat lisätty Gitin master branchiin
  
- **Gitissä** tehdään taskille sen alussa uusi branch. Gitin commitit tehdään imperatiivimuodossa, esim. "add tests for new attendance" tai "refactor URL scheme". Huomaa, että commit-messaget ja koodi kirjoitetaan aina englanniksi! Pikaohjeet Gitin käytöstä:
  * Otetaan uusin master branch: git pull, git checkout master (2 erillistä komentoa)
  * Uusi branch: git checkout -b *branch_name*
  * Tiedosto valmiina committia varten: git add *file_name*
  * Commitataan tiedosto: git commit -m "*kuvaus commitista*"
  * Pushataan commit GitHubiin: git push -u origin *branch_name* 
  * Kun taski on valmis ja kaikki sen commitit ovat GitHubissa, tehdään GitHubissa pull request.
  
