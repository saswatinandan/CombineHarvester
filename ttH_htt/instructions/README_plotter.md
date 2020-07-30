# Description of the used configs

- Plot ranges in top/bottom plots, make not to be log-scale and labels are coded by channel [here]9https://github.com/HEP-KBFI/CombineHarvester/blob/fd6a86d02f87b0746601c6850805f27c2bafed0d/ttH_htt/configs/plot_options_HH.py#L104-L129
- Stack processes naming, drawing style, drawing order, labels in legend, processes to merge (look eg how VH and TH are merged) are set globally [here](https://github.com/HEP-KBFI/CombineHarvester/blob/fd6a86d02f87b0746601c6850805f27c2bafed0d/ttH_htt/configs/plot_options_HH.py#L104-L129)


IMPORTANT: you need to ssh with "ssh -XY" to that working, and let the canvases pop-up. With "ssh -XYC" the plotter maybe run faster.
That is why we cannot now make that faster / as jobs / in screen right now.
