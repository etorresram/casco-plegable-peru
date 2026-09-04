# -*- coding: utf-8 -*-
USD_PEN = 3.3645
JPY_PEN = 0.021604
JPY_USD = JPY_PEN / USD_PEN          # PEN per JPY / PEN per USD
USD_JPY = 1/JPY_USD

PESO_UNIT = 0.62      # kg empacado
CBM_UNIT  = 0.005     # m3 empacado (plegado 22.2x29.7x6.3 + carton)

print(f"USD/PEN {USD_PEN}  |  JPY/PEN {JPY_PEN}  |  USD/JPY {USD_JPY:.1f}")
print()

def escenario(nombre, n, fob_u, flete, seguro_pct, arancel_pct, gastos_locales,
              igv_recuperable=True, otros=0):
    fob = n*fob_u
    seguro = fob*seguro_pct
    cif = fob + flete + seguro
    arancel = cif*arancel_pct
    igv = (cif+arancel)*0.18
    desembolso = cif + arancel + igv + gastos_locales + otros
    costo_real = desembolso - (igv if igv_recuperable else 0)
    print(f"--- {nombre}  (n={n})")
    print(f"  FOB               US$ {fob:9,.0f}   ({fob_u:.2f}/u)")
    print(f"  Flete+seguro      US$ {flete+seguro:9,.0f}")
    print(f"  CIF               US$ {cif:9,.0f}")
    print(f"  Arancel {arancel_pct*100:>4.0f}%      US$ {arancel:9,.0f}")
    print(f"  IGV 18%           US$ {igv:9,.0f}  {'(recuperable)' if igv_recuperable else '(costo)'}")
    print(f"  Gastos locales    US$ {gastos_locales+otros:9,.0f}")
    print(f"  ------------------------------------")
    print(f"  CAJA NECESARIA    US$ {desembolso:9,.0f}   = S/ {desembolso*USD_PEN:,.0f}")
    print(f"  Costo unit real   US$ {costo_real/n:9,.2f}   = S/ {costo_real/n*USD_PEN:,.0f}")
    for mk in (2.0, 2.5, 3.0):
        print(f"     PVP x{mk}: S/ {costo_real/n*USD_PEN*mk:,.0f}   margen bruto/u S/ {costo_real/n*USD_PEN*(mk-1):,.0f}")
    print()
    return costo_real/n

# Precios de origen
izano_retail_extax = 6598*JPY_USD          # Monotaro sin impuesto
izano_dist_est     = 6598*0.55*JPY_USD     # supuesto: 55% de lista como distribuidor
print(f"IZANO2 retail JP sin imp. = JPY 6,598 = US$ {izano_retail_extax:.2f} = S/ {6598*JPY_PEN:.0f}")
print(f"IZANO2 estimado distribuidor (55% lista) = US$ {izano_dist_est:.2f}")
print()

# A. Piloto courier desde Japon comprando a precio de tienda
escenario("A. PILOTO courier Japon, 45u a precio tienda", 45, izano_retail_extax,
          flete=45*0.85*20.11, seguro_pct=0.01, arancel_pct=0.04,
          gastos_locales=0, igv_recuperable=False)

# B. Piloto courier desde Japon con precio distribuidor
escenario("B. PILOTO courier Japon, 100u precio distribuidor(est)", 100, izano_dist_est,
          flete=100*0.85*20.11, seguro_pct=0.01, arancel_pct=0.04,
          gastos_locales=0, igv_recuperable=True)

# C. LCL Japon 300u precio distribuidor, EPA 0%
escenario("C. LCL Japon 300u distribuidor, EPA 0%", 300, izano_dist_est,
          flete=450, seguro_pct=0.01, arancel_pct=0.00,
          gastos_locales=700, igv_recuperable=True)

# D. China maquila carga compartida 150u a US$16 FOB
escenario("D. China 150u FOB US$16 carga compartida", 150, 16,
          flete=390, seguro_pct=0.01, arancel_pct=0.11,
          gastos_locales=190, igv_recuperable=True)

# E. China 500u FOB 14
escenario("E. China 500u FOB US$14 (2.5 CBM)", 500, 14,
          flete=390+120*2, seguro_pct=0.01, arancel_pct=0.11,
          gastos_locales=190+300, igv_recuperable=True)
