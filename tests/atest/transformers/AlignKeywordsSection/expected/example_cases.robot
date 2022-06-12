*** Settings ***
Documentation               This file contains examples of preferred output when run with command
...                         robotidy --transform AlignKeywordsSection:widths=24,28,20,20:compact_overflow=True example_cases.robot
...                         Exception is the  test "Examples where alignment to second column of Documentation text part would be nice to be possible" 
...                         where optional preferred output is in the next test below that 

*** Test Cases ***

Exclude whole multiline case by rule "Should_Not_Be_None"
    Should_Not_Be_None      ${NIMIKEKUVAUS}   ${HINTA_OCC_ULKOINEN}   ${MITTAYKSIKKÖ}  ${NIMIKETYYPPI_OCC}  ${OSANUMERO}
    ...                     ${NIMIKE}  ${MÄÄRÄ}   ${MITTAYKSIKKÖ}   ${LÄHETYSOSOITE_OCC}   ${LASKUTUSOSOITE_OCC}


Multiple return values ability to prevent alignment for return values
    ${HINTA_YKSI}  ${HINTA_RIVI}  ${HINTA_TILAUS_ALV}  ${toimituspvm}=
    ...                     TiHa_MyyntitilausTarkista_Tiedot
    ...                     ${TILAUS_FUSION}            ${NIMIKE}           ${NIMIKEKUVAUS}     ${MÄÄRÄ}            ${MITTAYKSIKKÖ}     ${TILAUSPVM}
    ...                     ${ASIAKAS}                  ${ASIAKAS_ID}       ${LÄHETYSOSOITE}    ${LÄHETYSTAPA}      ${LASKUTUSOSOITE}
    ...                     ${LIIKEYKSIKKÖ}             ${TILAAJA}          tila_tilaus=Käsittelyssä                tila_tilausrivi=Odottaa lähetystä
    ...                     lähde=${LÄHDE}              hinta_yks=${HINTA_YKSI}                 hinta_rivi=${HINTA_RIVI}
