# Description of the used configs

- Plot ranges in top/bottom plots, make not to be log-scale and labels are coded by channel [here](https://github.com/HEP-KBFI/CombineHarvester/blob/fd6a86d02f87b0746601c6850805f27c2bafed0d/ttH_htt/configs/plot_options_HH.py#L104-L129)
- Stack processes naming, drawing style, drawing order, labels in legend, processes to merge (look eg how VH and TH are merged) are set globally [here](https://github.com/HEP-KBFI/CombineHarvester/blob/fd6a86d02f87b0746601c6850805f27c2bafed0d/ttH_htt/configs/plot_options_HH.py#L104-L129)
- The list of processes that the plotter look is hardcoded by channel [here](https://github.com/HEP-KBFI/CombineHarvester/blob/ee10ff510cc31486704a4bf3b7ea1dd5821c15eb/ttH_htt/configs/list_channels_HH.py#L80-L92). Like this, you have the power of asking for a process not be drawn (if eg, have almost negligible yield).
 - if you see blanks between the total error band an the stack it is problably because a process if missing from this list (and problably as well from the ordered dictionary that makes the stack)
- The choice of the HH signal to draw makes effect [here](https://github.com/HEP-KBFI/CombineHarvester/blob/ee10ff510cc31486704a4bf3b7ea1dd5821c15eb/ttH_htt/configs/list_channels_HH.py#L80-L92).
 - Note that it supports having make a renaming, see the making of the cards for GF nonresonant NLO [here]() to understand why that.

Note: If you add processes to the datacards that are not in this list (eg ggH and qqH) you need to explicitly add on the above-mentioned places.

IMPORTANT: you need to ssh with "ssh -XY" to that working, and let the canvases pop-up. With "ssh -XYC" the plotter maybe run faster.
That is why we cannot now make that faster / as jobs / in screen right now.
