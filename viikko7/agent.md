Päätyikö agentti toimivaan ratkaisuun? Joo, se sai sen pystyyn loppujen lopuks. Aluks oli vähän säätöä riippuvuuksien ja porttien kanssa, mut se Flask-käyttöliittymä sieltä sit tuli ja peliä pysty klikkailemaan selaimessa.

Miten varmistuit, että ratkaisu toimii? No mä vaan klikkailin sitä selainta. Valitsin eri moodeja ja katoin et se oikeesti päivittää ne voitot sinne ruudulle.

Oletko ihan varma, että ratkaisu toimii oikein? en oo ihan sata varma mut vaikuttaa oikeelta.

Kuinka paljon jouduit antamaan agentille komentoja matkan varrella? Kolme promptia taisin käyttää ei niin paha.

Kuinka hyvät agentit tekemät testit olivat? Ne oli yllättävän kattavia. Se testas ne perusjutut et peli alkaa ja sit se simuloi niitä HTTP-pyyntöjä sinne endpointteihin.

Onko agentin tekemä koodi ymmärrettävää? Ihan ok, mut se heitti sinne sekaan kaikkia session-hallintoja ja Flask-juttuja mitä en ois ite keksiny.

Miten agentti on muuttanut edellisessä tehtävässä tekemääsi koodia? Se joutu muuttaa sitä pelaa()-metodia aika paljon. Alkuperäinen template method oli tehty terminaalille, mut agentti joutu pätkimään sitä, et se toimii stateless-tyyliin webissä.

Mitä uutta opit? Että agentti on aika hyvä korjaamaan omat virheensä jos sille antaa tarpeeks hyvää palautetta. Ja et web-sovelluksen ja terminaalisovelluksen logiikka on aika erilaista, vaikka se peruspeli oiski sama.