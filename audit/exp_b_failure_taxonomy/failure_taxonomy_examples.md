# Exp B failure-taxonomy examples

Examples are selected from existing frozen score rows and judge rationales.
They are illustrative diagnostics, not new scoring decisions.

## execution_failure (230)

- `s01` / Sonnet / DID: Error in waldtest(pretrend_model, "treated:period_2 = treated:period_3 = 0") : could not find function "waldtest" Calls: suppressMessages -> withCallingHandlers Execution halted
- `s01` / Gemini / DID: Error in tidy(event_study_model) : could not find function "tidy" Calls: suppressMessages -> withCallingHandlers -> as.data.frame Execution halted
- `s01` / GPT-5 / DID: Error in linearHypothesis.lm(mod_es, lead_params, vcov. = vc_es, test = "Chisq") : there are aliased coefficients in the model. Calls: suppressMessages ... withCallingHandlers -> <Anonymous> -> lin

## no_code_or_unparseable (44)

- `s08` / Gemini / DID: ## 1. Identification Strategy The research question aims to determine if the adoption of algorithmic credit scoring (fintech) reduced loan default rates. Given the panel data structure where banks adopt the technology at different points in time (simplified...
- `s09` / Gemini / DID: ## 1. Identification Strategy The research question asks whether a corporate tax cut (effective from period 4) differentially affected investment for large versus small firms. We have panel data on firms over time, with large firms (`treated = 1`) experienc...
- `s10` / Gemini / DID: ## 1. Identification Strategy The research question investigates whether banks pre-emptively raise capital ratios between the announcement of a new minimum capital requirement (period 3) and its effective date (period 5). This scenario is perfectly suited f...

## executed_wrong_coefficient (26)

- `s02` / Kimi / DID: The treatment effect coefficient is the Estimate for treat_x_post from the coeftest output, which is 0.244583.
- `s04` / Kimi / DID: The treatment effect coefficient is the Estimate for treat_x_post from the coeftest output, which is 0.524496.
- `s22` / Kimi / IV: The IV estimate coefficient on the endogenous regressor x is directly printed in stdout as 'IV estimate: 1.148109'

## coefficient_not_reported (15)

- `s06` / Kimi / DID: The stdout is empty; no coefficient table or estimate values are displayed in the output.
- `s28` / Kimi / RDD: The rdrobust output failed to print coefficient values; all coefficient results appear as empty or NULL, indicating the model did not produce valid estimates.
- `s67` / Kimi / IV: The stdout only shows the Breusch-Pagan test results; the actual coefficient estimates from the IV regression or second stage were not printed to stdout.

## event_window_or_scale_mismatch (11)

- `s12` / Opus / EVENT_STUDY: The main treatment effect is the mean CAR (Cumulative Abnormal Return) over the post-event window [0,+1], which is -4.8533% as reported in the main result section.
- `s13` / Opus / EVENT_STUDY: The treatment effect is the mean CAR[-1,+1] (cumulative abnormal return over the event window), which is -3.1758% as reported in the CAR[-1,+1] Summary Statistics section.
- `s51` / Kimi / EVENT_STUDY: The output shows day-by-day abnormal returns for individual event days, but does not provide a single aggregate treatment-effect coefficient for the post-event period (event_day >= 0). The script lack

## iv_first_stage_or_wrong_stage (5)

- `s19` / GPT-4o / IV: The stdout only shows the first-stage F-statistic; the 2SLS regression results table with the treatment coefficient on x is not printed in the output.
- `s21` / Kimi / IV: The second-stage coefficient on predicted veteran status (the instrumented treatment variable) is -30.00338, which represents the IV/2SLS treatment effect of military service on log annual earnings.
- `s69` / GPT-4o / IV: The stdout contains only diagnostic test results and first-stage regression output, but does not include the coefficient table from the IV regression itself showing the treatment effect on y.

## rdd_cutoff_or_sign_convention (3)

- `s27` / GPT-5 / RDD: The main local linear RD estimate (triangular kernel, p=1, h=0.1) reported in the output shows tau_hat = -0.1566, which is the primary treatment-effect coefficient for the sharp RDD at cutoff 0.5.
- `s29` / GPT-5 / RDD: The main RDD treatment effect coefficient is tau = -0.3599 from the local linear regression at the primary cutoff (c=0.5, h=0.10), shown in the Main estimate output and confirmed in the summary line a
- `s98` / GPT-5 / RDD: The main RD estimate (local linear, triangular kernel) at the estimated cutoff with bandwidth h=0.0499 shows tau = 0.5513, which is the treatment-effect coefficient for the covenant violation impact o

## wrong_target_variable (2)

- `s16` / GPT-4o / EVENT_STUDY: The script performs a cross-sectional regression of CAR on chip_dependency rather than estimating a post-event treatment effect coefficient; it reports the chip_dependency slope (-0.014632) but not an
- `s62` / Opus / EVENT_STUDY: The treatment-effect coefficient from the cross-sectional regression (CAR[-1,+1] on treatment indicator) is the 'treated' coefficient of 0.015969, which rounds to 0.0160.

## bandwidth_or_statistic_only (2)

- `s89` / GPT-4o / RDD: The rdrobust output shows only summary statistics (sample sizes, bandwidth parameters, kernel type) but does not display the coefficient table with the treatment effect estimate.
- `s100` / GPT-4o / RDD: The stdout displays only summary statistics and bandwidth information from rdrobust, but does not include the coefficient table with the treatment effect estimate.

## pretrend_or_placebo_coefficient (1)

- `s05` / GPT-4o / DID: The output shows only the pre-trends placebo test results, not the main DID model coefficients; the treated:post interaction term is missing.

## wrong_did_interaction (1)

- `s33` / GPT-4o / DID: The output does not contain the treated:post interaction coefficient; it only shows treated and post as separate main effects, and the interaction term is missing from the displayed results.
