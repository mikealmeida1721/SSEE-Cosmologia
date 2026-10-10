#!/bin/bash
# Cola 2026-10-10: re-sellar por DVC las etapas desactualizadas por el re-sellado de
# cmb_dbic_tau_ajustado y R1R2 (tanda pesada pendiente desde el 10-04). Secuencial:
# una etapa a la vez (perfil_h0_ancla usa 6 núcleos; DES continua ya usa 2).
cd /home/mike/Proyectos/SSEE
L=results/logs/cola_1010.log
for s in termino_volumen_boss marginal_vs_perfil perfil_wc_boss perfil_wc_boss_lcdm \
         cmb_ns_forzado cmb_wb_forzado cmb_dbic_mnu_propia paper4_toe sello_sn_geometria \
         leer_conjunta sello_erosita_conteos_erass1 sello_erosita_conteos_efeds sello_erosita_cr_v3 \
         perfil_h0_ancla lcdm_conjunta_min_cmb lcdm_conjunta_min_kids lcdm_conjunta_min_bao \
         lcdm_conjunta_min_conjunta lcdm_conjunta_control lcdm_conjunta_lee auditoria_pdfs_zenodo \
         des_y3_nla; do
  echo "[$(date +%F' '%T)] INICIO $s" >> $L
  .venv/bin/dvc repro -s $s >> $L 2>&1; echo "[$(date +%F' '%T)] FIN $s rc=$?" >> $L
done
echo "[$(date +%F' '%T)] COLA TERMINADA (faltan: des_y3_tatt al terminar continua, sondas_ssee_vs_lcdm, valores_tex)" >> $L
