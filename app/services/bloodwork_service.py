"""Bloodwork service for business logic."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.db.repositories.bloodwork_repository import BloodworkRepository
from app.models.bloodwork import Bloodwork



def _rr(low: float, high: float) -> dict[str, float]:
    return {"low": low, "optimal_low": low, "optimal_high": high, "high": high}


PANEL_TEMPLATES: list[dict[str, Any]] = []

PANEL_TEMPLATES.extend(
    [
        {
            "key": "vitals",
            "name": "Vitals / Anthropometrics",
            "markers": [
                {
                    "name": "Height",
                    "key": "height",
                    "unit": "cm",
                    "reference_note": "No standard reference range (individual measurement).",
                },
                {
                    "name": "Weight",
                    "key": "weight",
                    "unit": "kg",
                    "reference_note": "No standard reference range (individual measurement).",
                },
                {
                    "name": "BMI",
                    "key": "bmi",
                    "unit": "kg/m^2",
                    "reference_range": _rr(18.5, 24.9),
                },
                {
                    "name": "Waist circumference",
                    "key": "waist_circumference",
                    "unit": "cm",
                    "reference_note": "Men <94 cm (low risk), <102 cm (high risk); Women <80 cm (low risk), <88 cm (high risk).",
                },
                {
                    "name": "Hip circumference",
                    "key": "hip_circumference",
                    "unit": "cm",
                    "reference_note": "No standalone reference range.",
                },
                {
                    "name": "Waist:Hip ratio",
                    "key": "waist_hip_ratio",
                    "reference_note": "Men <0.90; Women <0.85 (low risk).",
                },
                {
                    "name": "Blood pressure - Systolic",
                    "key": "bp_systolic",
                    "unit": "mmHg",
                    "reference_note": "Optimal <130 mmHg; normal <140 mmHg (UK NICE).",
                },
                {
                    "name": "Blood pressure - Diastolic",
                    "key": "bp_diastolic",
                    "unit": "mmHg",
                    "reference_note": "Optimal <80 mmHg; normal <90 mmHg (UK NICE).",
                },
                {
                    "name": "Resting heart rate",
                    "key": "resting_heart_rate",
                    "unit": "bpm",
                    "reference_range": _rr(60, 100),
                },
                {
                    "name": "SpO2",
                    "key": "spo2",
                    "unit": "%",
                    "reference_range": _rr(95, 100),
                },
                {
                    "name": "Temperature",
                    "key": "temperature",
                    "unit": "C",
                    "reference_range": _rr(36.1, 37.2),
                },
            ],
        },
    ]
)

PANEL_TEMPLATES.extend(
    [
        {
            "key": "infectious",
            "name": "Infectious Disease Screen",
            "markers": [
                {
                    "name": "HIV Ag/Ab",
                    "key": "hiv_ag_ab",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Hepatitis B surface Ag",
                    "key": "hep_b_surface_ag",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Hepatitis B surface Ab",
                    "key": "hep_b_surface_ab",
                    "value_type": "text",
                    "reference_note": "Positive/immune.",
                },
                {
                    "name": "Hepatitis B core Ab",
                    "key": "hep_b_core_ab",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Hepatitis C Ab",
                    "key": "hep_c_ab",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Hepatitis C PCR (optional)",
                    "key": "hep_c_pcr",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Syphilis serology",
                    "key": "syphilis_serology",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Chlamydia NAAT",
                    "key": "chlamydia_naat",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Gonorrhea NAAT",
                    "key": "gonorrhea_naat",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
            ],
        },
        {
            "key": "fertility",
            "name": "Fertility (Semen Analysis)",
            "markers": [
                {
                    "name": "Semen volume",
                    "key": "semen_volume",
                    "unit": "mL",
                    "reference_note": ">1.5 mL.",
                },
                {
                    "name": "Semen pH",
                    "key": "semen_ph",
                    "reference_range": _rr(7.2, 8.0),
                },
                {
                    "name": "Sperm concentration",
                    "key": "sperm_concentration",
                    "unit": "million/mL",
                    "reference_note": ">15 million/mL.",
                },
                {
                    "name": "Total sperm count",
                    "key": "total_sperm_count",
                    "unit": "million",
                    "reference_note": ">39 million.",
                },
                {
                    "name": "Motility (total)",
                    "key": "motility_total",
                    "unit": "%",
                    "reference_note": ">40% total.",
                },
                {
                    "name": "Motility (progressive)",
                    "key": "motility_progressive",
                    "unit": "%",
                    "reference_note": ">32% progressive.",
                },
                {
                    "name": "Morphology",
                    "key": "morphology",
                    "unit": "%",
                    "reference_note": ">4% normal forms.",
                },
                {
                    "name": "Vitality",
                    "key": "vitality",
                    "unit": "%",
                    "reference_note": ">58% live.",
                },
                {
                    "name": "Semen WBCs",
                    "key": "semen_wbcs",
                    "unit": "million/mL",
                    "reference_range": _rr(0, 1),
                },
                {
                    "name": "DNA fragmentation (optional)",
                    "key": "dna_fragmentation",
                    "unit": "%",
                    "reference_range": _rr(0, 30),
                },
            ],
        },
    ]
)

PANEL_TEMPLATES.extend(
    [
        {
            "key": "coagulation",
            "name": "Coagulation",
            "markers": [
                {
                    "name": "PT",
                    "key": "pt",
                    "unit": "seconds",
                    "reference_range": _rr(10, 14),
                },
                {
                    "name": "INR",
                    "key": "inr_coag",
                    "reference_range": _rr(0.8, 1.2),
                },
                {
                    "name": "aPTT",
                    "key": "aptt",
                    "unit": "seconds",
                    "reference_range": _rr(25, 35),
                },
                {
                    "name": "D-dimer (optional)",
                    "key": "d_dimer",
                    "unit": "ng/mL",
                    "reference_range": _rr(0, 500),
                },
            ],
        },
        {
            "key": "cardiac",
            "name": "Cardiac Risk / Injury",
            "markers": [
                {
                    "name": "hs-Troponin (T or I)",
                    "key": "troponin",
                    "unit": "ng/L",
                    "reference_range": _rr(0, 14),
                },
                {
                    "name": "CK",
                    "key": "ck",
                    "unit": "U/L",
                    "reference_range": _rr(0, 200),
                },
                {
                    "name": "BNP or NT-proBNP",
                    "key": "bnp",
                    "unit": "pg/mL",
                    "reference_range": _rr(0, 100),
                },
                {
                    "name": "Homocysteine (optional)",
                    "key": "homocysteine",
                    "unit": "umol/L",
                    "reference_range": _rr(0, 15),
                },
            ],
        },
    ]
)

PANEL_TEMPLATES.extend(
    [
        {
            "key": "prostate",
            "name": "Prostate / Men's Screening",
            "markers": [
                {
                    "name": "PSA (total)",
                    "key": "psa_total",
                    "unit": "ng/mL",
                    "reference_note": "Age dependent; commonly <4 ng/mL.",
                },
                {
                    "name": "PSA (free)",
                    "key": "psa_free",
                    "unit": "ng/mL",
                    "reference_note": "Varies by lab.",
                },
                {
                    "name": "% Free PSA",
                    "key": "psa_free_percent",
                    "unit": "%",
                    "reference_note": ">25% lower risk.",
                },
            ],
        },
        {
            "key": "urinalysis",
            "name": "Urinalysis (Dip + Microscopy)",
            "markers": [
                {
                    "name": "Specific gravity",
                    "key": "specific_gravity",
                    "reference_range": _rr(1.005, 1.030),
                },
                {
                    "name": "pH",
                    "key": "ph",
                    "reference_range": _rr(5, 8),
                },
                {
                    "name": "Protein",
                    "key": "urine_protein",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Glucose",
                    "key": "urine_glucose",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Ketones",
                    "key": "urine_ketones",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Blood",
                    "key": "urine_blood",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Leukocyte esterase",
                    "key": "urine_leukocyte_esterase",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Nitrite",
                    "key": "urine_nitrite",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Bilirubin",
                    "key": "urine_bilirubin",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Urobilinogen",
                    "key": "urine_urobilinogen",
                    "value_type": "text",
                    "reference_note": "Normal/low.",
                },
                {
                    "name": "RBCs (microscopy)",
                    "key": "urine_rbcs",
                    "unit": "/HPF",
                    "reference_range": _rr(0, 5),
                },
                {
                    "name": "WBCs (microscopy)",
                    "key": "urine_wbcs",
                    "unit": "/HPF",
                    "reference_range": _rr(0, 5),
                },
                {
                    "name": "Casts",
                    "key": "urine_casts",
                    "value_type": "text",
                    "reference_note": "None/few.",
                },
                {
                    "name": "Crystals",
                    "key": "urine_crystals",
                    "value_type": "text",
                    "reference_note": "None/few.",
                },
                {
                    "name": "Bacteria/yeast",
                    "key": "urine_bacteria",
                    "value_type": "text",
                    "reference_note": "None.",
                },
                {
                    "name": "Epithelial cells",
                    "key": "urine_epithelial_cells",
                    "value_type": "text",
                    "reference_note": "Few.",
                },
                {
                    "name": "Urine culture (optional)",
                    "key": "urine_culture",
                    "value_type": "text",
                    "reference_note": "No growth.",
                },
            ],
        },
    ]
)

PANEL_TEMPLATES.extend(
    [
        {
            "key": "iron_studies",
            "name": "Iron Studies",
            "markers": [
                {
                    "name": "Ferritin",
                    "key": "ferritin_iron",
                    "unit": "ug/L",
                    "reference_note": "Men 30-400; Women 15-150 ug/L.",
                },
                {
                    "name": "Serum iron",
                    "key": "serum_iron",
                    "unit": "umol/L",
                    "reference_range": _rr(10, 30),
                },
                {
                    "name": "Transferrin",
                    "key": "transferrin",
                    "unit": "g/L",
                    "reference_range": _rr(2.0, 3.6),
                },
                {
                    "name": "TIBC",
                    "key": "tibc",
                    "unit": "umol/L",
                    "reference_range": _rr(45, 80),
                },
                {
                    "name": "Transferrin saturation",
                    "key": "transferrin_saturation",
                    "unit": "%",
                    "reference_range": _rr(20, 50),
                },
            ],
        },
        {
            "key": "vitamins",
            "name": "Vitamins / Minerals / Nutrition",
            "markers": [
                {
                    "name": "25-OH Vitamin D",
                    "key": "vitamin_d",
                    "unit": "nmol/L",
                    "reference_note": ">50 nmol/L (sufficient).",
                },
                {
                    "name": "Vitamin B12",
                    "key": "vitamin_b12",
                    "unit": "ng/L",
                    "reference_range": _rr(200, 900),
                },
                {
                    "name": "Folate (serum)",
                    "key": "folate_serum",
                    "unit": "ug/L",
                    "reference_note": ">4 ug/L.",
                },
                {
                    "name": "RBC folate (optional)",
                    "key": "rbc_folate",
                    "unit": "ug/L",
                    "reference_note": ">300 ug/L.",
                },
                {
                    "name": "Zinc",
                    "key": "zinc",
                    "unit": "umol/L",
                    "reference_range": _rr(11, 18),
                },
                {
                    "name": "Copper",
                    "key": "copper",
                    "unit": "umol/L",
                    "reference_range": _rr(11, 25),
                },
                {
                    "name": "Selenium (optional)",
                    "key": "selenium",
                    "unit": "umol/L",
                    "reference_note": "Varies by lab.",
                },
            ],
        },
    ]
)

PANEL_TEMPLATES.extend(
    [
        {
            "key": "adrenal",
            "name": "Adrenal / Stress",
            "markers": [
                {
                    "name": "Cortisol (AM)",
                    "key": "cortisol_am",
                    "unit": "nmol/L",
                    "reference_range": _rr(140, 690),
                    "reference_note": "140-690 nmol/L (morning).",
                },
                {
                    "name": "Cortisol (PM) (optional)",
                    "key": "cortisol_pm",
                    "unit": "nmol/L",
                    "reference_range": _rr(0, 100),
                    "reference_note": "<100 nmol/L (evening).",
                },
                {
                    "name": "ACTH",
                    "key": "acth",
                    "unit": "ng/L",
                    "reference_range": _rr(0, 50),
                    "reference_note": "<50 ng/L (morning).",
                },
                {
                    "name": "Aldosterone (optional)",
                    "key": "aldosterone",
                    "unit": "pmol/L",
                    "reference_note": "Varies by posture and assay.",
                },
                {
                    "name": "Renin (optional)",
                    "key": "renin",
                    "unit": "mU/L",
                    "reference_note": "Varies by posture and assay.",
                },
                {
                    "name": "Plasma metanephrines (optional)",
                    "key": "plasma_metanephrines",
                    "value_type": "text",
                    "reference_note": "Low/negative.",
                },
                {
                    "name": "Urine metanephrines (optional)",
                    "key": "urine_metanephrines",
                    "value_type": "text",
                    "reference_note": "Low/negative.",
                },
            ],
        },
        {
            "key": "inflammation",
            "name": "Inflammation / Immune",
            "markers": [
                {
                    "name": "hs-CRP",
                    "key": "hs_crp",
                    "unit": "mg/L",
                    "reference_range": _rr(0, 3),
                },
                {
                    "name": "CRP",
                    "key": "crp",
                    "unit": "mg/L",
                    "reference_range": _rr(0, 10),
                },
                {
                    "name": "ESR",
                    "key": "esr_inflammation",
                    "unit": "mm/hr",
                    "reference_note": "Men <15; Women <20 (age adjusted).",
                },
                {
                    "name": "Fibrinogen",
                    "key": "fibrinogen",
                    "unit": "g/L",
                    "reference_range": _rr(2, 4),
                },
                {
                    "name": "Ferritin",
                    "key": "ferritin_inflammation",
                    "unit": "ug/L",
                    "reference_note": "Men 30-400; Women 15-150 ug/L.",
                },
                {
                    "name": "GlycA (optional)",
                    "key": "glyca",
                    "unit": "umol/L",
                    "reference_note": "Varies by lab.",
                },
                {
                    "name": "IL-6 (optional)",
                    "key": "il6",
                    "unit": "pg/mL",
                    "reference_range": _rr(0, 7),
                },
            ],
        },
    ]
)

PANEL_TEMPLATES.extend(
    [
        {
            "key": "thyroid",
            "name": "Thyroid",
            "markers": [
                {
                    "name": "TSH",
                    "key": "tsh",
                    "unit": "mIU/L",
                    "reference_range": _rr(0.3, 4.2),
                },
                {
                    "name": "Free T4",
                    "key": "free_t4",
                    "unit": "pmol/L",
                    "reference_range": _rr(12, 22),
                },
                {
                    "name": "Free T3",
                    "key": "free_t3",
                    "unit": "pmol/L",
                    "reference_range": _rr(3.1, 6.8),
                },
                {
                    "name": "Total T4",
                    "key": "total_t4",
                    "unit": "nmol/L",
                    "reference_range": _rr(60, 160),
                },
                {
                    "name": "Total T3",
                    "key": "total_t3",
                    "unit": "nmol/L",
                    "reference_range": _rr(1.3, 3.1),
                },
                {
                    "name": "TPO antibodies",
                    "key": "tpo_antibodies",
                    "unit": "IU/mL",
                    "reference_range": _rr(0, 35),
                },
                {
                    "name": "Thyroglobulin antibodies",
                    "key": "thyroglobulin_antibodies",
                    "unit": "IU/mL",
                    "reference_range": _rr(0, 115),
                },
                {
                    "name": "TRAb / TSI (optional)",
                    "key": "trab_tsi",
                    "value_type": "text",
                    "reference_note": "Negative.",
                },
                {
                    "name": "Reverse T3 (optional)",
                    "key": "reverse_t3",
                    "unit": "pmol/L",
                    "reference_note": "Varies by lab.",
                },
            ],
        },
        {
            "key": "male_hormones",
            "name": "Male Hormones / Androgens",
            "markers": [
                {
                    "name": "Total testosterone (LC/MS if available)",
                    "key": "total_testosterone",
                    "unit": "nmol/L",
                    "reference_range": _rr(8.7, 29),
                },
                {
                    "name": "Free testosterone (calc or measured)",
                    "key": "free_testosterone",
                    "unit": "nmol/L",
                    "reference_range": _rr(0.2, 0.6),
                },
                {
                    "name": "SHBG",
                    "key": "shbg",
                    "unit": "nmol/L",
                    "reference_range": _rr(10, 57),
                },
                {
                    "name": "Sensitive estradiol (E2)",
                    "key": "estradiol",
                    "unit": "pmol/L",
                    "reference_range": _rr(0, 150),
                },
                {
                    "name": "LH",
                    "key": "lh",
                    "unit": "IU/L",
                    "reference_range": _rr(1, 9),
                },
                {
                    "name": "FSH",
                    "key": "fsh",
                    "unit": "IU/L",
                    "reference_range": _rr(1, 10),
                },
                {
                    "name": "Prolactin",
                    "key": "prolactin",
                    "unit": "mIU/L",
                    "reference_range": _rr(0, 400),
                },
                {
                    "name": "DHT",
                    "key": "dht",
                    "unit": "nmol/L",
                    "reference_range": _rr(1.0, 3.0),
                },
                {
                    "name": "DHEA-S",
                    "key": "dhea_s",
                    "unit": "umol/L",
                    "reference_range": _rr(5, 10),
                    "reference_note": "Age-dependent reference intervals.",
                },
                {
                    "name": "Androstenedione",
                    "key": "androstenedione",
                    "unit": "nmol/L",
                    "reference_range": _rr(2, 10),
                },
                {
                    "name": "Progesterone",
                    "key": "progesterone",
                    "unit": "nmol/L",
                    "reference_range": _rr(0, 5),
                },
                {
                    "name": "Pregnenolone",
                    "key": "pregnenolone",
                    "unit": "nmol/L",
                    "reference_note": "Varies by lab.",
                },
                {
                    "name": "IGF-1",
                    "key": "igf_1",
                    "unit": "nmol/L",
                    "reference_note": "Age dependent (e.g., 10-40 nmol/L adult).",
                },
                {
                    "name": "hCG (optional)",
                    "key": "hcg",
                    "unit": "IU/L",
                    "reference_range": _rr(0, 5),
                },
                {
                    "name": "Inhibin B (optional)",
                    "key": "inhibin_b",
                    "unit": "pg/mL",
                    "reference_note": "Varies by lab.",
                },
            ],
        },
    ]
)

PANEL_TEMPLATES.extend(
    [
        {
            "key": "lipids",
            "name": "Lipids (Standard + Advanced)",
            "markers": [
                {
                    "name": "Total cholesterol",
                    "key": "total_cholesterol",
                    "unit": "mmol/L",
                    "reference_range": _rr(0, 5.0),
                },
                {
                    "name": "LDL-C",
                    "key": "ldl_c",
                    "unit": "mmol/L",
                    "reference_range": _rr(0, 3.0),
                },
                {
                    "name": "HDL-C",
                    "key": "hdl_c",
                    "unit": "mmol/L",
                    "reference_note": "Men >1.0; Women >1.2 mmol/L.",
                },
                {
                    "name": "Triglycerides",
                    "key": "triglycerides",
                    "unit": "mmol/L",
                    "reference_range": _rr(0, 1.7),
                },
                {
                    "name": "Non-HDL cholesterol",
                    "key": "non_hdl_cholesterol",
                    "unit": "mmol/L",
                    "reference_range": _rr(0, 4.0),
                },
                {
                    "name": "ApoB",
                    "key": "apo_b",
                    "unit": "g/L",
                    "reference_range": _rr(0, 1.0),
                },
                {
                    "name": "ApoA1",
                    "key": "apo_a1",
                    "unit": "g/L",
                    "reference_note": "Men >1.0; Women >1.2 g/L.",
                },
                {
                    "name": "Lp(a)",
                    "key": "lpa",
                    "unit": "mg/dL",
                    "reference_range": _rr(0, 50),
                    "reference_note": "<50 mg/dL (or nmol/L equivalent).",
                },
                {
                    "name": "LDL-P (NMR) (optional)",
                    "key": "ldl_p",
                    "unit": "nmol/L",
                    "reference_note": "Varies by method.",
                },
                {
                    "name": "Small dense LDL (optional)",
                    "key": "small_dense_ldl",
                    "reference_note": "Varies by method.",
                },
                {
                    "name": "hs-CRP (lipids)",
                    "key": "hs_crp_lipids",
                    "unit": "mg/L",
                    "reference_range": _rr(0, 3),
                },
            ],
        },
        {
            "key": "glucose_insulin",
            "name": "Glucose / Insulin / Diabetes",
            "markers": [
                {
                    "name": "Fasting glucose",
                    "key": "fasting_glucose",
                    "unit": "mmol/L",
                    "reference_range": _rr(3.0, 6.0),
                },
                {
                    "name": "Fasting insulin",
                    "key": "fasting_insulin",
                    "unit": "mIU/L",
                    "reference_note": "Varies (often 2-25 mIU/L).",
                },
                {
                    "name": "HbA1c",
                    "key": "hba1c",
                    "unit": "mmol/mol",
                    "reference_range": _rr(0, 42),
                    "reference_note": "<42 mmol/mol (6.0%) non-diabetic.",
                },
                {
                    "name": "C-peptide",
                    "key": "c_peptide",
                    "unit": "nmol/L",
                    "reference_range": _rr(0.3, 1.3),
                },
                {
                    "name": "Fructosamine",
                    "key": "fructosamine",
                    "unit": "umol/L",
                    "reference_range": _rr(200, 285),
                },
                {
                    "name": "OGTT glucose (0 min)",
                    "key": "ogtt_glucose_0",
                    "unit": "mmol/L",
                    "reference_range": _rr(0, 6.1),
                },
                {
                    "name": "OGTT glucose (60 min) (optional)",
                    "key": "ogtt_glucose_60",
                    "unit": "mmol/L",
                    "reference_note": "Varies by protocol.",
                },
                {
                    "name": "OGTT glucose (120 min) (optional)",
                    "key": "ogtt_glucose_120",
                    "unit": "mmol/L",
                    "reference_range": _rr(0, 7.8),
                },
                {
                    "name": "OGTT insulin (0 min) (optional)",
                    "key": "ogtt_insulin_0",
                    "unit": "mIU/L",
                    "reference_note": "Varies by protocol.",
                },
                {
                    "name": "OGTT insulin (60 min) (optional)",
                    "key": "ogtt_insulin_60",
                    "unit": "mIU/L",
                    "reference_note": "Varies by protocol.",
                },
                {
                    "name": "OGTT insulin (120 min) (optional)",
                    "key": "ogtt_insulin_120",
                    "unit": "mIU/L",
                    "reference_note": "Varies by protocol.",
                },
            ],
        },
    ]
)

PANEL_TEMPLATES.extend(
    [
        {
            "key": "liver_extended",
            "name": "Liver / Hepatobiliary Extended",
            "markers": [
                {
                    "name": "GGT",
                    "key": "ggt",
                    "unit": "U/L",
                    "reference_note": "Men <55; Women <38 U/L.",
                },
                {
                    "name": "LDH",
                    "key": "ldh",
                    "unit": "U/L",
                    "reference_range": _rr(135, 225),
                },
                {
                    "name": "INR",
                    "key": "inr",
                    "reference_range": _rr(0.8, 1.2),
                },
            ],
        },
        {
            "key": "kidney_extended",
            "name": "Kidney / Renal Extended",
            "markers": [
                {
                    "name": "Cystatin C",
                    "key": "cystatin_c",
                    "unit": "mg/L",
                    "reference_range": _rr(0.6, 1.0),
                    "reference_note": "0.6-1.0 mg/L (age-dependent).",
                },
                {
                    "name": "eGFR (cystatin-based)",
                    "key": "egfr_cystatin",
                    "unit": "mL/min/1.73m^2",
                    "reference_note": ">90 mL/min/1.73m^2 (normal).",
                },
                {
                    "name": "Uric acid",
                    "key": "uric_acid",
                    "unit": "umol/L",
                    "reference_note": "Men 200-420; Women 140-360 umol/L.",
                },
                {
                    "name": "Phosphate",
                    "key": "phosphate",
                    "unit": "mmol/L",
                    "reference_range": _rr(0.8, 1.5),
                },
                {
                    "name": "Magnesium",
                    "key": "magnesium",
                    "unit": "mmol/L",
                    "reference_range": _rr(0.7, 1.0),
                },
                {
                    "name": "Urine albumin (microalbumin)",
                    "key": "urine_albumin",
                    "unit": "mg/L",
                    "reference_range": _rr(0, 30),
                },
                {
                    "name": "Urine creatinine",
                    "key": "urine_creatinine",
                    "unit": "mmol/L",
                    "reference_note": "Varies by hydration.",
                },
                {
                    "name": "Albumin:Creatinine Ratio (ACR)",
                    "key": "acr",
                    "unit": "mg/mmol",
                    "reference_range": _rr(0, 3),
                },
                {
                    "name": "Protein:Creatinine Ratio (PCR)",
                    "key": "pcr",
                    "unit": "mg/mmol",
                    "reference_range": _rr(0, 15),
                },
            ],
        },
    ]
)

PANEL_TEMPLATES.extend(
    [
        {
            "key": "bmp",
            "name": "Basic Metabolic Panel (BMP)",
            "markers": [
                {
                    "name": "Sodium",
                    "key": "sodium",
                    "unit": "mmol/L",
                    "reference_range": _rr(135, 145),
                },
                {
                    "name": "Potassium",
                    "key": "potassium",
                    "unit": "mmol/L",
                    "reference_range": _rr(3.5, 5.3),
                },
                {
                    "name": "Chloride",
                    "key": "chloride",
                    "unit": "mmol/L",
                    "reference_range": _rr(95, 105),
                },
                {
                    "name": "CO2 / Bicarbonate",
                    "key": "bicarbonate",
                    "unit": "mmol/L",
                    "reference_range": _rr(22, 29),
                },
                {
                    "name": "Anion gap",
                    "key": "anion_gap",
                    "unit": "mmol/L",
                    "reference_range": _rr(8, 16),
                },
                {
                    "name": "Glucose (fasting)",
                    "key": "glucose_fasting",
                    "unit": "mmol/L",
                    "reference_range": _rr(3.0, 6.0),
                },
                {
                    "name": "Urea (or BUN)",
                    "key": "urea",
                    "unit": "mmol/L",
                    "reference_range": _rr(2.5, 7.8),
                },
                {
                    "name": "Creatinine",
                    "key": "creatinine",
                    "unit": "umol/L",
                    "reference_note": "Men 60-110; Women 45-90 umol/L.",
                },
                {
                    "name": "eGFR",
                    "key": "egfr",
                    "unit": "mL/min/1.73m^2",
                    "reference_note": ">90 mL/min/1.73m^2 (normal; staged for CKD).",
                },
                {
                    "name": "Calcium",
                    "key": "calcium",
                    "unit": "mmol/L",
                    "reference_range": _rr(2.10, 2.60),
                },
            ],
        },
        {
            "key": "cmp_addons",
            "name": "Comprehensive Metabolic Panel Add-ons (CMP)",
            "markers": [
                {
                    "name": "Albumin",
                    "key": "albumin",
                    "unit": "g/L",
                    "reference_range": _rr(35, 50),
                },
                {
                    "name": "Total protein",
                    "key": "total_protein",
                    "unit": "g/L",
                    "reference_range": _rr(60, 80),
                },
                {
                    "name": "Globulin",
                    "key": "globulin",
                    "unit": "g/L",
                    "reference_range": _rr(20, 35),
                },
                {
                    "name": "A/G ratio",
                    "key": "ag_ratio",
                    "reference_range": _rr(1.0, 2.0),
                },
                {
                    "name": "Total bilirubin",
                    "key": "total_bilirubin",
                    "unit": "umol/L",
                    "reference_range": _rr(0, 21),
                },
                {
                    "name": "Direct bilirubin",
                    "key": "direct_bilirubin",
                    "unit": "umol/L",
                    "reference_range": _rr(0, 5),
                },
                {
                    "name": "ALP",
                    "key": "alp",
                    "unit": "U/L",
                    "reference_range": _rr(30, 130),
                },
                {
                    "name": "ALT",
                    "key": "alt",
                    "unit": "U/L",
                    "reference_range": _rr(0, 50),
                },
                {
                    "name": "AST",
                    "key": "ast",
                    "unit": "U/L",
                    "reference_range": _rr(0, 50),
                },
            ],
        },
    ]
)

PANEL_TEMPLATES.extend(
    [
        {
            "key": "cbc",
            "name": "Hematology (CBC)",
            "markers": [
                {
                    "name": "White blood cell count (WBC)",
                    "key": "wbc",
                    "unit": "x10^9/L",
                    "reference_range": _rr(4.0, 11.0),
                },
                {
                    "name": "Red blood cell count (RBC)",
                    "key": "rbc",
                    "unit": "x10^12/L",
                    "reference_note": "Men 4.5-5.5; Women 3.8-4.8 x10^12/L.",
                },
                {
                    "name": "Hemoglobin",
                    "key": "hemoglobin",
                    "unit": "g/L",
                    "reference_note": "Men 130-180; Women 120-150 g/L.",
                },
                {
                    "name": "Hematocrit",
                    "key": "hematocrit",
                    "unit": "L/L",
                    "reference_note": "Men 0.40-0.50; Women 0.36-0.46.",
                },
                {
                    "name": "MCV",
                    "key": "mcv",
                    "unit": "fL",
                    "reference_range": _rr(80, 100),
                },
                {
                    "name": "MCH",
                    "key": "mch",
                    "unit": "pg",
                    "reference_range": _rr(27, 32),
                },
                {
                    "name": "MCHC",
                    "key": "mchc",
                    "unit": "g/L",
                    "reference_range": _rr(320, 360),
                },
                {
                    "name": "RDW",
                    "key": "rdw",
                    "unit": "%",
                    "reference_range": _rr(11, 15),
                },
                {
                    "name": "Platelet count",
                    "key": "platelets",
                    "unit": "x10^9/L",
                    "reference_range": _rr(150, 400),
                },
                {
                    "name": "MPV",
                    "key": "mpv",
                    "unit": "fL",
                    "reference_range": _rr(7, 11),
                },
                {
                    "name": "Neutrophils (absolute)",
                    "key": "neutrophils_abs",
                    "unit": "x10^9/L",
                    "reference_range": _rr(2.0, 7.5),
                },
                {
                    "name": "Neutrophils (%)",
                    "key": "neutrophils_pct",
                    "unit": "%",
                    "reference_range": _rr(40, 75),
                },
                {
                    "name": "Lymphocytes (absolute)",
                    "key": "lymphocytes_abs",
                    "unit": "x10^9/L",
                    "reference_range": _rr(1.0, 3.0),
                },
                {
                    "name": "Lymphocytes (%)",
                    "key": "lymphocytes_pct",
                    "unit": "%",
                    "reference_range": _rr(20, 45),
                },
                {
                    "name": "Monocytes (absolute)",
                    "key": "monocytes_abs",
                    "unit": "x10^9/L",
                    "reference_range": _rr(0.2, 1.0),
                },
                {
                    "name": "Monocytes (%)",
                    "key": "monocytes_pct",
                    "unit": "%",
                    "reference_range": _rr(2, 10),
                },
                {
                    "name": "Eosinophils (absolute)",
                    "key": "eosinophils_abs",
                    "unit": "x10^9/L",
                    "reference_range": _rr(0.0, 0.4),
                },
                {
                    "name": "Eosinophils (%)",
                    "key": "eosinophils_pct",
                    "unit": "%",
                    "reference_range": _rr(1, 6),
                },
                {
                    "name": "Basophils (absolute)",
                    "key": "basophils_abs",
                    "unit": "x10^9/L",
                    "reference_range": _rr(0.0, 0.1),
                },
                {
                    "name": "Basophils (%)",
                    "key": "basophils_pct",
                    "unit": "%",
                    "reference_range": _rr(0, 1),
                },
                {
                    "name": "Immature granulocytes (absolute)",
                    "key": "immature_granulocytes_abs",
                    "unit": "x10^9/L",
                    "reference_range": _rr(0.0, 0.1),
                },
                {
                    "name": "Immature granulocytes (%)",
                    "key": "immature_granulocytes_pct",
                    "unit": "%",
                    "reference_range": _rr(0, 1),
                },
                {
                    "name": "Reticulocytes (absolute)",
                    "key": "reticulocytes_abs",
                    "unit": "x10^12/L",
                    "reference_range": _rr(0.05, 0.1),
                },
                {
                    "name": "Reticulocytes (%)",
                    "key": "reticulocytes_pct",
                    "unit": "%",
                    "reference_range": _rr(0.5, 1.5),
                },
                {
                    "name": "Nucleated RBCs",
                    "key": "nucleated_rbcs",
                    "value_type": "text",
                    "reference_note": "0 / 100 WBC.",
                },
                {
                    "name": "ESR",
                    "key": "esr",
                    "unit": "mm/hr",
                    "reference_note": "Men <15; Women <20 (age adjusted).",
                },
            ],
        }
    ]
)


@dataclass
class MarkerSummary:
    """Summary counts for marker status."""

    total: int
    out_of_range: int


class BloodworkService:
    """Service for bloodwork-related business logic."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.bloodwork_repo = BloodworkRepository(db)

    def get_published_results(self, patient_id: int) -> list[Bloodwork]:
        """Return published bloodwork results for a patient."""
        return self.bloodwork_repo.get_published_for_patient(patient_id)

    @staticmethod
    def _has_value(value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        return True

    def get_panel_templates(self) -> list[dict[str, Any]]:
        """Return panel templates for creating results."""
        return PANEL_TEMPLATES

    def get_panel_template(self, panel_key: str) -> dict[str, Any]:
        """Return a single panel template."""
        for panel in PANEL_TEMPLATES:
            if panel["key"] == panel_key:
                return panel
        raise ValueError(f"Unknown panel key: {panel_key}")

    def build_panel_results(
        self, panel: dict[str, Any], values: dict[str, float | str]
    ) -> dict[str, Any]:
        """Build a bloodwork results payload for a panel."""
        markers = []
        for marker in panel.get("markers", []):
            marker_key = marker.get("key", marker.get("name"))
            if marker_key not in values:
                continue
            value = values.get(marker_key)
            if not self._has_value(value):
                continue
            markers.append(
                {
                    "name": marker.get("name", ""),
                    "abbreviation": marker.get("abbreviation", ""),
                    "value": value,
                    "unit": marker.get("unit", ""),
                    "reference_range": marker.get("reference_range", {}),
                    "reference_note": marker.get("reference_note", ""),
                }
            )
        return {
            "test_name": panel.get("name", "Bloodwork Panel"),
            "categories": [{"name": panel.get("name", "Panel"), "markers": markers}],
        }

    def create_draft_result(
        self,
        patient_id: int,
        panel_key: str,
        test_date: date,
        values: dict[str, float | str],
    ) -> Bloodwork:
        """Create an unpublished bloodwork result."""
        panel = self.get_panel_template(panel_key)
        results = self.build_panel_results(panel, values)
        return self.bloodwork_repo.create(
            patient_id=patient_id,
            test_type=panel.get("name", "Bloodwork Panel"),
            test_date=test_date,
            results=results,
            reference_ranges={},
            notes=None,
            is_published=False,
            approved_by=None,
            approved_at=None,
            published_at=None,
        )

    def publish_result(
        self, bloodwork_id: int, doctor_id: int, signature: str, notes: str | None
    ) -> Bloodwork | None:
        """Publish a bloodwork result."""
        bloodwork = self.bloodwork_repo.get_by_id(bloodwork_id)
        if not bloodwork:
            return None

        now = datetime.now(timezone.utc)
        results = bloodwork.results or {}
        if isinstance(results, dict):
            review = results.get("review", {})
            review["signature"] = signature
            review["signed_at"] = now.isoformat()
            results["review"] = review
            bloodwork.results = results

        if notes:
            bloodwork.notes = notes

        bloodwork.is_published = True
        bloodwork.approved_by = doctor_id
        bloodwork.approved_at = now
        bloodwork.published_at = now
        return self.bloodwork_repo.save(bloodwork)

    def normalize_bloodwork(self, bloodwork: Bloodwork) -> dict[str, Any]:
        """Normalize bloodwork payloads into a common structure."""
        results = bloodwork.results or {}
        if isinstance(results, dict) and "categories" in results:
            categories = []
            for category in results.get("categories", []):
                markers = [
                    marker
                    for marker in category.get("markers", [])
                    if self._has_value(marker.get("value"))
                ]
                if not markers:
                    continue
                payload = dict(category)
                payload["markers"] = markers
                categories.append(payload)
            return {
                "test_name": results.get("test_name") or bloodwork.test_type,
                "categories": categories,
            }

        markers = []
        reference_ranges = bloodwork.reference_ranges or {}
        for name, value in results.items():
            if not self._has_value(value):
                continue
            reference_range = self._parse_reference_range(reference_ranges.get(name))
            markers.append(
                {
                    "name": name,
                    "abbreviation": name,
                    "value": value,
                    "unit": "",
                    "reference_range": reference_range,
                }
            )
        return {
            "test_name": bloodwork.test_type,
            "categories": [{"name": "Results", "markers": markers}],
        }

    def summarize_categories(self, categories: list[dict[str, Any]]) -> MarkerSummary:
        """Return total markers and out-of-range count."""
        total = 0
        out_of_range = 0
        for category in categories:
            markers = category.get("markers", [])
            markers = [m for m in markers if self._has_value(m.get("value"))]
            total += len(markers)
            for marker in markers:
                status = self.get_marker_status(marker)
                if status in {"low", "high", "critical"}:
                    out_of_range += 1
        return MarkerSummary(total=total, out_of_range=out_of_range)

    def summarize_category(self, category: dict[str, Any]) -> MarkerSummary:
        """Return summary for a single category."""
        markers = [
            m for m in category.get("markers", []) if self._has_value(m.get("value"))
        ]
        total = len(markers)
        out_of_range = sum(
            1
            for marker in markers
            if self.get_marker_status(marker) in {"low", "high", "critical"}
        )
        return MarkerSummary(total=total, out_of_range=out_of_range)

    def get_marker_status(self, marker: dict[str, Any]) -> str:
        """Return a normalized marker status."""
        status = marker.get("status")
        if isinstance(status, str) and status:
            return status.lower()

        reference = marker.get("reference_range") or {}
        try:
            value = float(marker.get("value"))
        except (TypeError, ValueError):
            return "unknown"

        low = reference.get("low")
        high = reference.get("high")
        optimal_low = reference.get("optimal_low", low)
        optimal_high = reference.get("optimal_high", high)

        if low is None or high is None:
            return "unknown"

        try:
            low = float(low)
            high = float(high)
            if optimal_low is not None:
                optimal_low = float(optimal_low)
            if optimal_high is not None:
                optimal_high = float(optimal_high)
        except (TypeError, ValueError):
            return "unknown"

        if value < low or value > high:
            return "critical"
        if optimal_low is not None and value < optimal_low:
            return "low"
        if optimal_high is not None and value > optimal_high:
            return "high"
        return "normal"

    def _parse_reference_range(self, raw_range: Any) -> dict[str, float]:
        if isinstance(raw_range, dict):
            return raw_range
        if isinstance(raw_range, str):
            parts = raw_range.replace(" ", "").split("-")
            if len(parts) == 2:
                try:
                    low = float(parts[0])
                    high = float(parts[1])
                except ValueError:
                    return {}
                return {
                    "low": low,
                    "optimal_low": low,
                    "optimal_high": high,
                    "high": high,
                }
        return {}
