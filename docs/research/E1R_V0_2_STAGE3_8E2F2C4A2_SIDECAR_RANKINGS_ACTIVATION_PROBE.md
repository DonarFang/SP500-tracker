# Stage 3.8E-2F-2C-4A-2 Sidecar Rankings Activation Probe

Generated At: `2026-07-08T13:07:55.802211+00:00`

## Status

- Status: `SIDECAR_RANKINGS_ACTIVATION_PROBE_COMPLETE_NO_EXPORTS_WRITTEN`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Diagnosis

- records_count=1260; subclass_counts={'NO_SUBCLASS': 1019, 'MA_CONFLICT': 135, 'DETERIORATION_TRANSITION': 63, 'RECOVERY_TRANSITION': 43}; active_by_subclass={}.
- raw_record_keys=['candidate_count', 'date', 'gross_exposure', 'holdings', 'is_active', 'next_date', 'portfolio_return', 'portfolio_return_pct', 'regime', 'selected_count', 'spx_return', 'spx_return_pct', 'subclass'].
- selected_key_counter={'holdings': 1350}.
- MA_CONFLICT ranking stats={'rankings_summary': {'type': 'dict', 'len': 241, 'keys': ['2022-01-24', '2022-01-25', '2022-01-26', '2022-01-27', '2022-01-28', '2022-01-31', '2022-02-01', '2022-02-02', '2022-02-03', '2022-02-04', '2022-02-14', '2022-02-15', '2022-02-16', '2022-02-17', '2022-02-18', '2022-02-22', '2022-02-23', '2022-02-24', '2022-02-25', '2022-02-28', '2022-03-01', '2022-03-02', '2022-03-03', '2022-03-04', '2022-03-07', '2022-03-08', '2022-03-09', '2022-03-10', '2022-03-11', '2022-03-14', '2022-03-15', '2022-03-16', '2022-03-17', '2022-03-18', '2022-03-21', '2022-03-22', '2022-03-23', '2022-03-24', '2022-03-25', '2022-03-28', '2022-03-29', '2022-03-30', '2022-03-31', '2022-04-01', '2022-04-04', '2022-04-05', '2022-04-06', '2022-04-07', '2022-04-08', '2022-04-11', '2022-04-12', '2022-04-13', '2022-04-14', '2022-04-18', '2022-04-19', '2022-04-20', '2022-04-21', '2022-04-22', '2022-04-25', '2022-04-26', '2022-04-27', '2022-04-28', '2022-04-29', '2022-05-02', '2022-05-03', '2022-05-04', '2022-05-05', '2022-05-06', '2022-05-09', '2022-05-10', '2022-05-11', '2022-05-12', '2022-05-13', '2022-05-16', '2022-05-17', '2022-05-18', '2022-05-19', '2022-05-20', '2022-12-05', '2022-12-06'], 'sample': [['2022-01-24', {'type': 'dict', 'len': 6, 'keys': ['candidate_count', 'candidates', 'date', 'next_date', 'regime', 'subclass'], 'sample': [['date', {'type': 'str', 'repr': "'2022-01-24'"}]]}], ['2022-01-25', {'type': 'dict', 'len': 6, 'keys': ['candidate_count', 'candidates', 'date', 'next_date', 'regime', 'subclass'], 'sample': [['date', {'type': 'str', 'repr': "'2022-01-25'"}]]}], ['2022-01-26', {'type': 'dict', 'len': 6, 'keys': ['candidate_count', 'candidates', 'date', 'next_date', 'regime', 'subclass'], 'sample': [['date', {'type': 'str', 'repr': "'2022-01-26'"}]]}]]}, 'ma_conflict_intervals': 135, 'ma_conflict_ranking_count_known': 0, 'ma_conflict_ranking_min': None, 'ma_conflict_ranking_max': None, 'ma_conflict_ranking_zero_count': 0, 'ma_conflict_ranking_unknown_count': 135}.
- MA_CONFLICT rankings are empty/unknown; likely ranking construction or date key mismatch blocks sidecar selection.

## Ranking Stats

```json
{
  "rankings_summary": {
    "type": "dict",
    "len": 241,
    "keys": [
      "2022-01-24",
      "2022-01-25",
      "2022-01-26",
      "2022-01-27",
      "2022-01-28",
      "2022-01-31",
      "2022-02-01",
      "2022-02-02",
      "2022-02-03",
      "2022-02-04",
      "2022-02-14",
      "2022-02-15",
      "2022-02-16",
      "2022-02-17",
      "2022-02-18",
      "2022-02-22",
      "2022-02-23",
      "2022-02-24",
      "2022-02-25",
      "2022-02-28",
      "2022-03-01",
      "2022-03-02",
      "2022-03-03",
      "2022-03-04",
      "2022-03-07",
      "2022-03-08",
      "2022-03-09",
      "2022-03-10",
      "2022-03-11",
      "2022-03-14",
      "2022-03-15",
      "2022-03-16",
      "2022-03-17",
      "2022-03-18",
      "2022-03-21",
      "2022-03-22",
      "2022-03-23",
      "2022-03-24",
      "2022-03-25",
      "2022-03-28",
      "2022-03-29",
      "2022-03-30",
      "2022-03-31",
      "2022-04-01",
      "2022-04-04",
      "2022-04-05",
      "2022-04-06",
      "2022-04-07",
      "2022-04-08",
      "2022-04-11",
      "2022-04-12",
      "2022-04-13",
      "2022-04-14",
      "2022-04-18",
      "2022-04-19",
      "2022-04-20",
      "2022-04-21",
      "2022-04-22",
      "2022-04-25",
      "2022-04-26",
      "2022-04-27",
      "2022-04-28",
      "2022-04-29",
      "2022-05-02",
      "2022-05-03",
      "2022-05-04",
      "2022-05-05",
      "2022-05-06",
      "2022-05-09",
      "2022-05-10",
      "2022-05-11",
      "2022-05-12",
      "2022-05-13",
      "2022-05-16",
      "2022-05-17",
      "2022-05-18",
      "2022-05-19",
      "2022-05-20",
      "2022-12-05",
      "2022-12-06"
    ],
    "sample": [
      [
        "2022-01-24",
        {
          "type": "dict",
          "len": 6,
          "keys": [
            "candidate_count",
            "candidates",
            "date",
            "next_date",
            "regime",
            "subclass"
          ],
          "sample": [
            [
              "date",
              {
                "type": "str",
                "repr": "'2022-01-24'"
              }
            ]
          ]
        }
      ],
      [
        "2022-01-25",
        {
          "type": "dict",
          "len": 6,
          "keys": [
            "candidate_count",
            "candidates",
            "date",
            "next_date",
            "regime",
            "subclass"
          ],
          "sample": [
            [
              "date",
              {
                "type": "str",
                "repr": "'2022-01-25'"
              }
            ]
          ]
        }
      ],
      [
        "2022-01-26",
        {
          "type": "dict",
          "len": 6,
          "keys": [
            "candidate_count",
            "candidates",
            "date",
            "next_date",
            "regime",
            "subclass"
          ],
          "sample": [
            [
              "date",
              {
                "type": "str",
                "repr": "'2022-01-26'"
              }
            ]
          ]
        }
      ]
    ]
  },
  "ma_conflict_intervals": 135,
  "ma_conflict_ranking_count_known": 0,
  "ma_conflict_ranking_min": null,
  "ma_conflict_ranking_max": null,
  "ma_conflict_ranking_zero_count": 0,
  "ma_conflict_ranking_unknown_count": 135
}
```

## Raw Record Keys

```json
[
  "candidate_count",
  "date",
  "gross_exposure",
  "holdings",
  "is_active",
  "next_date",
  "portfolio_return",
  "portfolio_return_pct",
  "regime",
  "selected_count",
  "spx_return",
  "spx_return_pct",
  "subclass"
]
```

## MA_CONFLICT Samples

```json
[
  {
    "record": {
      "date": "2022-01-24",
      "next_date": "2022-01-25",
      "regime": "SIDEWAYS",
      "subclass": "MA_CONFLICT",
      "is_active": true,
      "candidate_count": 526,
      "selected_count": 10,
      "gross_exposure": 0.25,
      "portfolio_return": 0.006639857390068424,
      "portfolio_return_pct": 0.6639857390068423,
      "spx_return": -0.012171906366504448,
      "spx_return_pct": -1.2171906366504448,
      "holdings": [
        {
          "symbol": "ATI",
          "score": 116.16247415664218,
          "weight": 0.025,
          "raw_return": -0.03076152294503265,
          "raw_return_pct": -3.076152294503265,
          "weighted_contribution": -0.0007690380736258163,
          "weighted_contribution_pct": -0.07690380736258162
        },
        {
          "symbol": "HAL",
          "score": 111.15001424870495,
          "weight": 0.025,
          "raw_return": 0.06995452837657856,
          "raw_return_pct": 6.995452837657856,
          "weighted_contribution": 0.001748863209414464,
          "weighted_contribution_pct": 0.1748863209414464
        },
        {
          "symbol": "SLB",
          "score": 106.92388446720653,
          "weight": 0.025,
          "raw_return": 0.05983634830107065,
          "raw_return_pct": 5.983634830107065,
          "weighted_contribution": 0.0014959087075267663,
          "weighted_contribution_pct": 0.14959087075267663
        },
        {
          "symbol": "XOM",
          "score": 100.24242388837584,
          "weight": 0.025,
          "raw_return": 0.029399762413809594,
          "raw_return_pct": 2.9399762413809594,
          "weighted_contribution": 0.0007349940603452399,
          "weighted_contribution_pct": 0.07349940603452398
        },
        {
          "symbol": "LVS",
          "score": 91.50122657304557,
          "weight": 0.025,
          "raw_return": -0.0004454036697800756,
          "raw_return_pct": -0.04454036697800756,
          "weighted_contribution": -1.113509174450189e-05,
          "weighted_contribution_pct": -0.001113509174450189
        },
        {
          "symbol": "EOG",
          "score": 86.66843612722552,
          "weight": 0.025,
          "raw_return": 0.04525474543965413,
          "raw_return_pct": 4.525474543965413,
          "weighted_contribution": 0.0011313686359913533,
          "weighted_contribution_pct": 0.11313686359913533
        },
        {
          "symbol": "KR",
          "score": 86.03641665380985,
          "weight": 0.025,
          "raw_return": -0.055322651935767575,
          "raw_return_pct": -5.532265193576757,
          "weighted_contribution": -0.0013830662983941894,
          "weighted_contribution_pct": -0.13830662983941894
        },
        {
          "symbol": "DVN",
          "score": 84.99916193288533,
          "weight": 0.025,
          "raw_return": 0.06062487833843444,
          "raw_return_pct": 6.062487833843444,
          "weighted_contribution": 0.001515621958460861,
          "weighted_contribution_pct": 0.1515621958460861
        },
        {
          "symbol": "COP",
          "score": 84.69324527256238,
          "weight": 0.025,
          "raw_return": 0.04926508363551951,
          "raw_return_pct": 4.926508363551951,
          "weighted_contribution": 0.001231627090887988,
          "weighted_contribution_pct": 0.1231627090887988
        },
        {
          "symbol": "PSX",
          "score": 79.62080082649405,
          "weight": 0.025,
          "raw_return": 0.03778852764825036,
          "raw_return_pct": 3.778852764825036,
          "weighted_contribution": 0.000944713191206259,
          "weighted_contribution_pct": 0.0944713191206259
        }
      ]
    },
    "ranking_len_for_date_or_next_date": null,
    "ranking_summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "candidate_count",
        "candidates",
        "date",
        "next_date",
        "regime",
        "subclass"
      ],
      "sample": [
        [
          "date",
          {
            "type": "str",
            "repr": "'2022-01-24'"
          }
        ],
        [
          "next_date",
          {
            "type": "str",
            "repr": "'2022-01-25'"
          }
        ]
      ]
    }
  },
  {
    "record": {
      "date": "2022-01-25",
      "next_date": "2022-01-26",
      "regime": "SIDEWAYS",
      "subclass": "MA_CONFLICT",
      "is_active": true,
      "candidate_count": 526,
      "selected_count": 10,
      "gross_exposure": 0.25,
      "portfolio_return": 0.001170111266206414,
      "portfolio_return_pct": 0.1170111266206414,
      "spx_return": -0.001496635725913631,
      "spx_return_pct": -0.1496635725913631,
      "holdings": [
        {
          "symbol": "HAL",
          "score": 151.45363429039952,
          "weight": 0.025,
          "raw_return": 0.006864893922020832,
          "raw_return_pct": 0.6864893922020832,
          "weighted_contribution": 0.0001716223480505208,
          "weighted_contribution_pct": 0.01716223480505208
        },
        {
          "symbol": "SLB",
          "score": 139.37639311786864,
          "weight": 0.025,
          "raw_return": 0.026037581179024105,
          "raw_return_pct": 2.6037581179024105,
          "weighted_contribution": 0.0006509395294756027,
          "weighted_contribution_pct": 0.06509395294756026
        },
        {
          "symbol": "APA",
          "score": 121.79645158380266,
          "weight": 0.025,
          "raw_return": 0.0012094774785773588,
          "raw_return_pct": 0.12094774785773588,
          "weighted_contribution": 3.023693696443397e-05,
          "weighted_contribution_pct": 0.003023693696443397
        },
        {
          "symbol": "DVN",
          "score": 117.26115304831168,
          "weight": 0.025,
          "raw_return": 0.010339429921368382,
          "raw_return_pct": 1.0339429921368382,
          "weighted_contribution": 0.00025848574803420953,
          "weighted_contribution_pct": 0.025848574803420954
        },
        {
          "symbol": "XOM",
          "score": 117.25739123090229,
          "weight": 0.025,
          "raw_return": -0.010142911282465361,
          "raw_return_pct": -1.0142911282465361,
          "weighted_contribution": -0.000253572782061634,
          "weighted_contribution_pct": -0.025357278206163403
        },
        {
          "symbol": "OXY",
          "score": 115.31360347380125,
          "weight": 0.025,
          "raw_return": 0.007887026148316378,
          "raw_return_pct": 0.7887026148316378,
          "weighted_contribution": 0.00019717565370790948,
          "weighted_contribution_pct": 0.01971756537079095
        },
        {
          "symbol": "EOG",
          "score": 113.90314776978222,
          "weight": 0.025,
          "raw_return": 0.005516989662422533,
          "raw_return_pct": 0.5516989662422533,
          "weighted_contribution": 0.00013792474156056335,
          "weighted_contribution_pct": 0.013792474156056335
        },
        {
          "symbol": "COP",
          "score": 111.51896168451287,
          "weight": 0.025,
          "raw_return": -0.000573591138362417,
          "raw_return_pct": -0.057359113836241704,
          "weighted_contribution": -1.4339778459060427e-05,
          "weighted_contribution_pct": -0.0014339778459060426
        },
        {
          "symbol": "ATI",
          "score": 109.39959091274764,
          "weight": 0.025,
          "raw_return": -0.003641987702496907,
          "raw_return_pct": -0.3641987702496907,
          "weighted_contribution": -9.104969256242268e-05,
          "weighted_contribution_pct": -0.009104969256242268
        },
        {
          "symbol": "FANG",
          "score": 102.91623878730167,
          "weight": 0.025,
          "raw_return": 0.0033075424598516534,
          "raw_return_pct": 0.33075424598516534,
          "weighted_contribution": 8.268856149629134e-05,
          "weighted_contribution_pct": 0.008268856149629134
        }
      ]
    },
    "ranking_len_for_date_or_next_date": null,
    "ranking_summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "candidate_count",
        "candidates",
        "date",
        "next_date",
        "regime",
        "subclass"
      ],
      "sample": [
        [
          "date",
          {
            "type": "str",
            "repr": "'2022-01-25'"
          }
        ],
        [
          "next_date",
          {
            "type": "str",
            "repr": "'2022-01-26'"
          }
        ]
      ]
    }
  },
  {
    "record": {
      "date": "2022-01-26",
      "next_date": "2022-01-27",
      "regime": "SIDEWAYS",
      "subclass": "MA_CONFLICT",
      "is_active": true,
      "candidate_count": 527,
      "selected_count": 10,
      "gross_exposure": 0.25,
      "portfolio_return": 0.0005712995435184164,
      "portfolio_return_pct": 0.05712995435184164,
      "spx_return": -0.005384088721519631,
      "spx_return_pct": -0.5384088721519631,
      "holdings": [
        {
          "symbol": "HAL",
          "score": 153.663382743099,
          "weight": 0.025,
          "raw_return": 0.0009740431199891653,
          "raw_return_pct": 0.09740431199891653,
          "weighted_contribution": 2.4351077999729134e-05,
          "weighted_contribution_pct": 0.002435107799972913
        },
        {
          "symbol": "SLB",
          "score": 149.8206298067245,
          "weight": 0.025,
          "raw_return": -0.02361818145681749,
          "raw_return_pct": -2.361818145681749,
          "weighted_contribution": -0.0005904545364204373,
          "weighted_contribution_pct": -0.05904545364204373
        },
        {
          "symbol": "APA",
          "score": 117.82183153229215,
          "weight": 0.025,
          "raw_return": -0.004832447111308369,
          "raw_return_pct": -0.4832447111308369,
          "weighted_contribution": -0.00012081117778270923,
          "weighted_contribution_pct": -0.012081117778270922
        },
        {
          "symbol": "DVN",
          "score": 117.24908488045658,
          "weight": 0.025,
          "raw_return": -0.0009652738498846514,
          "raw_return_pct": -0.09652738498846514,
          "weighted_contribution": -2.4131846247116286e-05,
          "weighted_contribution_pct": -0.0024131846247116284
        },
        {
          "symbol": "OXY",
          "score": 116.97373046933191,
          "weight": 0.025,
          "raw_return": 0.005396268303159646,
          "raw_return_pct": 0.5396268303159646,
          "weighted_contribution": 0.00013490670757899115,
          "weighted_contribution_pct": 0.013490670757899115
        },
        {
          "symbol": "EOG",
          "score": 116.84316316300695,
          "weight": 0.025,
          "raw_return": 0.020645559668631686,
          "raw_return_pct": 2.0645559668631686,
          "weighted_contribution": 0.0005161389917157921,
          "weighted_contribution_pct": 0.051613899171579214
        },
        {
          "symbol": "XOM",
          "score": 113.39783397463201,
          "weight": 0.025,
          "raw_return": 0.012808551203940421,
          "raw_return_pct": 1.2808551203940421,
          "weighted_contribution": 0.00032021378009851055,
          "weighted_contribution_pct": 0.032021378009851054
        },
        {
          "symbol": "COP",
          "score": 112.71257858494111,
          "weight": 0.025,
          "raw_return": 0.0298643853909617,
          "raw_return_pct": 2.98643853909617,
          "weighted_contribution": 0.0007466096347740425,
          "weighted_contribution_pct": 0.07466096347740425
        },
        {
          "symbol": "ATI",
          "score": 105.19917172050665,
          "weight": 0.025,
          "raw_return": -0.02715409921671008,
          "raw_return_pct": -2.715409921671008,
          "weighted_contribution": -0.0006788524804177521,
          "weighted_contribution_pct": -0.0678852480417752
        },
        {
          "symbol": "FANG",
          "score": 103.21173493250777,
          "weight": 0.025,
          "raw_return": 0.009733175688774631,
          "raw_return_pct": 0.9733175688774631,
          "weighted_contribution": 0.0002433293922193658,
          "weighted_contribution_pct": 0.024332939221936578
        }
      ]
    },
    "ranking_len_for_date_or_next_date": null,
    "ranking_summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "candidate_count",
        "candidates",
        "date",
        "next_date",
        "regime",
        "subclass"
      ],
      "sample": [
        [
          "date",
          {
            "type": "str",
            "repr": "'2022-01-26'"
          }
        ],
        [
          "next_date",
          {
            "type": "str",
            "repr": "'2022-01-27'"
          }
        ]
      ]
    }
  },
  {
    "record": {
      "date": "2022-01-27",
      "next_date": "2022-01-28",
      "regime": "SIDEWAYS",
      "subclass": "MA_CONFLICT",
      "is_active": true,
      "candidate_count": 528,
      "selected_count": 10,
      "gross_exposure": 0.25,
      "portfolio_return": 0.0002960625997241865,
      "portfolio_return_pct": 0.02960625997241865,
      "spx_return": 0.02434764687874269,
      "spx_return_pct": 2.434764687874269,
      "holdings": [
        {
          "symbol": "HAL",
          "score": 159.2712159909222,
          "weight": 0.025,
          "raw_return": 0.017191030257081463,
          "raw_return_pct": 1.7191030257081463,
          "weighted_contribution": 0.0004297757564270366,
          "weighted_contribution_pct": 0.04297757564270366
        },
        {
          "symbol": "SLB",
          "score": 137.7396523549379,
          "weight": 0.025,
          "raw_return": 0.021101362027854398,
          "raw_return_pct": 2.11013620278544,
          "weighted_contribution": 0.00052753405069636,
          "weighted_contribution_pct": 0.052753405069635995
        },
        {
          "symbol": "COP",
          "score": 133.358611221586,
          "weight": 0.025,
          "raw_return": -0.0049075204567661235,
          "raw_return_pct": -0.49075204567661235,
          "weighted_contribution": -0.0001226880114191531,
          "weighted_contribution_pct": -0.012268801141915309
        },
        {
          "symbol": "EOG",
          "score": 130.76771232181088,
          "weight": 0.025,
          "raw_return": -0.00045576549545711664,
          "raw_return_pct": -0.045576549545711664,
          "weighted_contribution": -1.1394137386427917e-05,
          "weighted_contribution_pct": -0.0011394137386427918
        },
        {
          "symbol": "OXY",
          "score": 125.62783807270606,
          "weight": 0.025,
          "raw_return": 0.008320502497189963,
          "raw_return_pct": 0.8320502497189963,
          "weighted_contribution": 0.00020801256242974908,
          "weighted_contribution_pct": 0.020801256242974908
        },
        {
          "symbol": "APA",
          "score": 125.47275274589161,
          "weight": 0.025,
          "raw_return": 0.006676701855573786,
          "raw_return_pct": 0.6676701855573786,
          "weighted_contribution": 0.00016691754638934465,
          "weighted_contribution_pct": 0.016691754638934464
        },
        {
          "symbol": "XOM",
          "score": 124.23625821580293,
          "weight": 0.025,
          "raw_return": 0.0021296909589767488,
          "raw_return_pct": 0.21296909589767488,
          "weighted_contribution": 5.324227397441872e-05,
          "weighted_contribution_pct": 0.005324227397441872
        },
        {
          "symbol": "DVN",
          "score": 121.67181237712464,
          "weight": 0.025,
          "raw_return": -0.003672396451885218,
          "raw_return_pct": -0.3672396451885218,
          "weighted_contribution": -9.180991129713046e-05,
          "weighted_contribution_pct": -0.009180991129713047
        },
        {
          "symbol": "FANG",
          "score": 109.20647341820883,
          "weight": 0.025,
          "raw_return": 0.0006218312166403894,
          "raw_return_pct": 0.06218312166403894,
          "weighted_contribution": 1.5545780416009737e-05,
          "weighted_contribution_pct": 0.0015545780416009738
        },
        {
          "symbol": "CVX",
          "score": 107.0591815922152,
          "weight": 0.025,
          "raw_return": -0.03516293242024082,
          "raw_return_pct": -3.516293242024082,
          "weighted_contribution": -0.0008790733105060206,
          "weighted_contribution_pct": -0.08790733105060206
        }
      ]
    },
    "ranking_len_for_date_or_next_date": null,
    "ranking_summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "candidate_count",
        "candidates",
        "date",
        "next_date",
        "regime",
        "subclass"
      ],
      "sample": [
        [
          "date",
          {
            "type": "str",
            "repr": "'2022-01-27'"
          }
        ],
        [
          "next_date",
          {
            "type": "str",
            "repr": "'2022-01-28'"
          }
        ]
      ]
    }
  },
  {
    "record": {
      "date": "2022-01-28",
      "next_date": "2022-01-31",
      "regime": "SIDEWAYS",
      "subclass": "MA_CONFLICT",
      "is_active": true,
      "candidate_count": 528,
      "selected_count": 10,
      "gross_exposure": 0.25,
      "portfolio_return": -0.0011961999291116743,
      "portfolio_return_pct": -0.11961999291116743,
      "spx_return": 0.01888595172426344,
      "spx_return_pct": 1.888595172426344,
      "holdings": [
        {
          "symbol": "HAL",
          "score": 163.62557477227205,
          "weight": 0.025,
          "raw_return": -0.01977040691587384,
          "raw_return_pct": -1.977040691587384,
          "weighted_contribution": -0.000494260172896846,
          "weighted_contribution_pct": -0.0494260172896846
        },
        {
          "symbol": "SLB",
          "score": 141.12604099229782,
          "weight": 0.025,
          "raw_return": -0.015372781267682045,
          "raw_return_pct": -1.5372781267682045,
          "weighted_contribution": -0.00038431953169205116,
          "weighted_contribution_pct": -0.03843195316920511
        },
        {
          "symbol": "EOG",
          "score": 128.3419757475321,
          "weight": 0.025,
          "raw_return": 0.016226324764806233,
          "raw_return_pct": 1.6226324764806233,
          "weighted_contribution": 0.00040565811912015584,
          "weighted_contribution_pct": 0.04056581191201558
        },
        {
          "symbol": "OXY",
          "score": 124.71014720361767,
          "weight": 0.025,
          "raw_return": 0.00266139347743799,
          "raw_return_pct": 0.266139347743799,
          "weighted_contribution": 6.653483693594975e-05,
          "weighted_contribution_pct": 0.006653483693594976
        },
        {
          "symbol": "COP",
          "score": 124.60327629851206,
          "weight": 0.025,
          "raw_return": -0.006724989345986754,
          "raw_return_pct": -0.6724989345986754,
          "weighted_contribution": -0.00016812473364966887,
          "weighted_contribution_pct": -0.016812473364966888
        },
        {
          "symbol": "APA",
          "score": 122.16277934243318,
          "weight": 0.025,
          "raw_return": 0.001206039154524996,
          "raw_return_pct": 0.1206039154524996,
          "weighted_contribution": 3.0150978863124903e-05,
          "weighted_contribution_pct": 0.0030150978863124904
        },
        {
          "symbol": "XOM",
          "score": 118.67381186747284,
          "weight": 0.025,
          "raw_return": 0.009033010424802868,
          "raw_return_pct": 0.9033010424802868,
          "weighted_contribution": 0.0002258252606200717,
          "weighted_contribution_pct": 0.02258252606200717
        },
        {
          "symbol": "DVN",
          "score": 110.86805612919885,
          
```

## Source Activation Lines

```json
[
  {
    "line": 10,
    "terms": [
      "MA_CONFLICT"
    ],
    "text": "- Active only in SIDEWAYS:MA_CONFLICT."
  },
  {
    "line": 44,
    "terms": [
      "allowed_subclasses",
      "MA_CONFLICT",
      "subclass"
    ],
    "text": "    allowed_subclasses: tuple[str, ...] = (\"MA_CONFLICT\",)"
  },
  {
    "line": 45,
    "terms": [
      "top_n"
    ],
    "text": "    top_n: int = 10"
  },
  {
    "line": 46,
    "terms": [
      "gross_exposure"
    ],
    "text": "    gross_exposure: float = 0.25"
  },
  {
    "line": 47,
    "terms": [
      "min_history"
    ],
    "text": "    min_history_days: int = 200"
  },
  {
    "line": 48,
    "terms": [
      "min_price"
    ],
    "text": "    min_price: float = 5.0"
  },
  {
    "line": 134,
    "terms": [
      "continue"
    ],
    "text": "            continue"
  },
  {
    "line": 172,
    "terms": [
      "continue"
    ],
    "text": "            continue"
  },
  {
    "line": 174,
    "terms": [
      "min_history"
    ],
    "text": "        if len(asset[\"bars\"]) < config.min_history_days:"
  },
  {
    "line": 175,
    "terms": [
      "continue"
    ],
    "text": "            continue"
  },
  {
    "line": 275,
    "terms": [
      "min_price"
    ],
    "text": "    if close is None or close < config.min_price:"
  },
  {
    "line": 356,
    "terms": [
      "rankings"
    ],
    "text": "def build_daily_rankings("
  },
  {
    "line": 363,
    "terms": [
      "rankings"
    ],
    "text": "    rankings: dict[str, dict[str, Any]] = {}"
  },
  {
    "line": 368,
    "terms": [
      "continue"
    ],
    "text": "            continue"
  },
  {
    "line": 374,
    "terms": [
      "continue"
    ],
    "text": "                continue"
  },
  {
    "line": 378,
    "terms": [
      "continue"
    ],
    "text": "                continue"
  },
  {
    "line": 382,
    "terms": [
      "continue"
    ],
    "text": "                continue"
  },
  {
    "line": 389,
    "terms": [
      "rankings"
    ],
    "text": "        rankings[date] = {"
  },
  {
    "line": 393,
    "terms": [
      "subclass"
    ],
    "text": "            \"subclass\": regime_info.get(\"subclass\") or \"NO_SUBCLASS\","
  },
  {
    "line": 398,
    "terms": [
      "rankings"
    ],
    "text": "    return rankings"
  },
  {
    "line": 402,
    "terms": [
      "rankings"
    ],
    "text": "    rankings: dict[str, dict[str, Any]],"
  },
  {
    "line": 408,
    "terms": [
      "allowed_subclasses",
      "subclass"
    ],
    "text": "    allowed_subclasses = set(config.allowed_subclasses)"
  },
  {
    "line": 409,
    "terms": [
      "top_n"
    ],
    "text": "    top_n = int(config.top_n)"
  },
  {
    "line": 410,
    "terms": [
      "gross_exposure"
    ],
    "text": "    gross_exposure = float(config.gross_exposure)"
  },
  {
    "line": 417,
    "terms": [
      "subclass"
    ],
    "text": "        subclass = regime_info.get(\"subclass\") or \"NO_SUBCLASS\""
  },
  {
    "line": 421,
    "terms": [
      "rankings"
    ],
    "text": "        ranked = rankings.get(date, {})"
  },
  {
    "line": 426,
    "terms": [
      "allowed_subclasses",
      "subclass"
    ],
    "text": "            and subclass in allowed_subclasses"
  },
  {
    "line": 427,
    "terms": [
      "top_n"
    ],
    "text": "            and top_n > 0"
  },
  {
    "line": 428,
    "terms": [
      "gross_exposure"
    ],
    "text": "            and gross_exposure > 0"
  },
  {
    "line": 436,
    "terms": [
      "selected",
      "top_n"
    ],
    "text": "            selected = candidates[:top_n]"
  },
  {
    "line": 437,
    "terms": [
      "selected",
      "gross_exposure"
    ],
    "text": "            weight = gross_exposure / len(selected)"
  },
  {
    "line": 439,
    "terms": [
      "selected"
    ],
    "text": "            for candidate in selected:"
  },
  {
    "line": 458,
    "terms": [
      "subclass"
    ],
    "text": "            \"subclass\": subclass,"
  },
  {
    "line": 461,
    "terms": [
      "selected"
    ],
    "text": "            \"selected_count\": len(holdings),"
  },
  {
    "line": 462,
    "terms": [
      "gross_exposure"
    ],
    "text": "            \"gross_exposure\": gross_exposure if is_active else 0.0,"
  },
  {
    "line": 498,
    "terms": [
      "MA_CONFLICT"
    ],
    "text": "        \"name\": \"E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
  },
  {
    "line": 499,
    "terms": [
      "allowed_subclasses",
      "subclass"
    ],
    "text": "        \"allowed_subclasses\": list(config.allowed_subclasses),"
  },
  {
    "line": 500,
    "terms": [
      "top_n"
    ],
    "text": "        \"top_n\": config.top_n,"
  },
  {
    "line": 501,
    "terms": [
      "gross_exposure"
    ],
    "text": "        \"gross_exposure\": config.gross_exposure,"
  },
  {
    "line": 549,
    "terms": [
      "rankings"
    ],
    "text": "    rankings = build_daily_rankings(stocks, spx, regimes, intervals, config)"
  },
  {
    "line": 550,
    "terms": [
      "rankings"
    ],
    "text": "    records = run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, config)"
  },
  {
    "line": 554,
    "terms": [
      "subclass"
    ],
    "text": "    subclass_counts: dict[str, int] = {}"
  },
  {
    "line": 558,
    "terms": [
      "subclass"
    ],
    "text": "        subclass = record[\"subclass\"]"
  },
  {
    "line": 561,
    "terms": [
      "subclass"
    ],
    "text": "            subclass_counts[subclass] = subclass_counts.get(subclass, 0) + 1"
  },
  {
    "line": 569,
    "terms": [
      "allowed_subclasses",
      "subclass"
    ],
    "text": "            \"allowed_subclasses\": list(config.allowed_subclasses),"
  },
  {
    "line": 570,
    "terms": [
      "top_n"
    ],
    "text": "            \"top_n\": config.top_n,"
  },
  {
    "line": 571,
    "terms": [
      "gross_exposure"
    ],
    "text": "            \"gross_exposure\": config.gross_exposure,"
  },
  {
    "line": 572,
    "terms": [
      "min_history"
    ],
    "text": "            \"min_history_days\": config.min_history_days,"
  },
  {
    "line": 573,
    "terms": [
      "min_price"
    ],
    "text": "            \"min_price\": config.min_price,"
  },
  {
    "line": 590,
    "terms": [
      "subclass"
    ],
    "text": "            \"sideways_subclass_counts\": subclass_counts,"
  }
]
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4A-3`: Patch sidecar export wrapper based on activation contract
- Recommended action: Use this probe to determine whether the wrapper needs date-key adaptation, selected-field adaptation, or explicit config. Do not modify frozen sidecar logic.

