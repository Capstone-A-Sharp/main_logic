class Calibration:
    def __init__(self):
        self.left_history = [] # 최근 값 저장
        self.right_history = [] # 최근 값 저장
        self.history_length = 10  # 최근 10번 값 기억
        self.threshold_min= 10  # 10 이내로 값이 변하면 안정됐다고 판단
        self.threshold_max= 30  # 30 이내로 값이 변하면 안정됐다고 판단   

    def calculate_minmax(self, context):
        left_sum = context.get('left_sum')
        right_sum = context.get('right_sum')

        # 최근 값 기록
        self.left_history.append(left_sum)
        self.right_history.append(right_sum)

        if len(self.left_history) > self.history_length:
            self.left_history.pop(0)
        if len(self.right_history) > self.history_length:
            self.right_history.pop(0)

        # 최솟값 안정 상태 판단
        if max(self.left_history) - min(self.left_history) < self.threshold_min:
            # 최솟값 갱신
            if context.get('left_min') > left_sum:
                context['left_min'] = left_sum 
            if context.get('right_min') > right_sum:
                context['right_min'] = right_sum

        # 최댓값 안정 상태 판단
        if max(self.right_history) - min(self.right_history) < self.threshold_max:
            # 최댓값 갱신
            if context.get('left_max') < left_sum:
                context['left_max'] = left_sum 
            if context.get('right_max') < right_sum:
                context['right_max'] = right_sum


