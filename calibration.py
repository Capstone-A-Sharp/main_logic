class Calibration:
    def __init__(self):
        pass
    
    def caculate_minmax(self,context):
        # 최솟값 갱신
        if context.get('left_min')>context.get('left_sum'):
            context['left_min']=context.get('left_sum')
        if context.get('right_min')>context.get('right_sum'):
            context['right_min']=context.get('right_sum')
            
        # 최댓값 갱신
        if context.get('left_max')<context.get('left_sum'):
            context['left_max']=context.get('left_sum')
        if context.get('right_max')<context.get('right_sum'):
            context['right_max']=context.get('right_sum')
           
            