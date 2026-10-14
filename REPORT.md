# Gorgias CX Report — Bike Shop (synthetic data)

- **Tickets analyzed:** 900
- **Median first response:** 1.8h (SLA 4h — breach rate 29.7%)
- **Median resolution:** 21.7h (SLA 48h — breach rate 20.3%)
- **CSAT:** 4.06/5 across 530 rated tickets
- **Peak hour:** 6:00 — schedule coverage here first

## Volume by channel
| channel   |   0 |
|:----------|----:|
| email     | 410 |
| chat      | 264 |
| phone     | 130 |
| sms       |  96 |

## Volume by tag
| tag           |   0 |
|:--------------|----:|
| sizing        | 189 |
| shipping      | 188 |
| order-status  | 134 |
| returns       | 133 |
| compatibility |  94 |
| warranty      |  92 |
| stock         |  70 |

## CSAT by tag (lowest first)
| tag           |   csat_score |
|:--------------|-------------:|
| warranty      |         3.67 |
| returns       |         3.73 |
| shipping      |         3.83 |
| sizing        |         4.19 |
| compatibility |         4.4  |
| order-status  |         4.42 |
| stock         |         4.43 |

## Median first response by tag (slowest first)
| tag           | frt_hours   |
|:--------------|:------------|
| order-status  | 2.0h        |
| shipping      | 1.9h        |
| stock         | 1.9h        |
| sizing        | 1.7h        |
| returns       | 1.7h        |
| compatibility | 1.7h        |
| warranty      | 1.6h        |

## Agent scorecard
| agent   |   tickets |   csat |
|:--------|----------:|-------:|
| Leo     |       202 |   4.07 |
| Maya    |       167 |   4.09 |
| Nora    |       177 |   4.01 |
| Priya   |       179 |   4.05 |
| Sam     |       175 |   4.1  |

## Recommendations
1. **'warranty'** has the lowest CSAT (3.67) — build
   Gorgias macros + a help-center article for the top 'warranty' questions.
2. **'order-status'** is slowest to first response (2.0h median) —
   add a tag-triggered auto-reply and route to the most technical agent.
3. Staff the **6:00** peak; move email backlog triage earlier in the day.
