# Tail-vs-utilization claim audit (R5)

Utilization was NOT independently manipulated (arrival rates/session length fixed); no-shows and arrival jitter only indirectly reduce effective load. The categorical claim 'tail rather than utilization' is not supported and must be softened.

tail_aware better than fixed_mean (fraction of specs):

|             |     0 |
|:------------|------:|
| (0.0, 0.0)  | 1     |
| (0.0, 2.0)  | 1     |
| (0.05, 0.0) | 0.667 |
| (0.05, 2.0) | 0.667 |
| (0.1, 0.0)  | 0.333 |
| (0.1, 2.0)  | 0.333 |
| (0.2, 0.0)  | 0     |
| (0.2, 2.0)  | 0     |

Honest framing: gains shrink as no-show rises (lower effective load) - consistent with a utilization channel we did not isolate.
