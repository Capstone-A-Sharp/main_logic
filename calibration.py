class Calibration:
    def __init__(self):
        self.left_history = []
        self.right_history = []
        self.history_length = 10 

    def reset_minmax(self,context):
        # 스위치 껐다가 켰을 때 
        context["left_min"] = 9999
        context["right_min"] = 9999
        context["left_max"] = -9999
        context["right_max"] = -9999
    
    def calculate_minmax(self, context):
        left_sum = context.get('left_sum')
        right_sum = context.get('right_sum')

        self.left_history.append(left_sum)
        self.right_history.append(right_sum)

        if len(self.left_history) > self.history_length:
            self.left_history.pop(0)
        if len(self.right_history) > self.history_length:
            self.right_history.pop(0)
    
        left_avg = sum(self.left_history) / len(self.left_history)*1.05
        right_avg = sum(self.right_history) / len(self.right_history)*1.05
                
        if context.get('left_min') > left_avg:
            context['left_min'] = left_avg
        if context.get('right_min') > right_avg: 
            context['right_min'] = right_avg



        context['left_min'] = min(context.get('left_min'), left_avg)
        context['right_min'] = min(context.get('right_min'), right_avg)
        context['left_max'] = max(context.get('left_max'), left_avg)
        context['right_max'] = max(context.get('right_max'), right_avg)
