SUBJECT = {
    'register_start': '会议注册开始通知',
    'register_due': '会议注册截止通知',
    'accept_due': '会议投稿截止通知',
    'modify_due': '修改稿投递截止通知',
    'first_passed': '恭喜',
    'first_rejected': '很遗憾',
    'first_modified': '论文修改通知',
}

MESSAGE = {
    'register_start': '尊敬的{0}：\n\n您收藏的会议{1}已经开放会议注册，如果您想参加该会议的话，请在{2}之前完成会议注册。\n\n本邮件为系统自动发送，请勿回复！',
    'register_due': '尊敬的{0}：\n\n您收藏的会议{1}即将到达会议注册截止日期，如果您想参加该会议的话，请在{2}之前完成会议注册。\n\n本邮件为系统自动发送，请勿回复！',
    'accept_due': '尊敬的{0}：\n\n您收藏的会议{1}即将到达投稿截止日期，如果您想向该会议进行投稿的话，请在{2}之前完成投稿。\n\n本邮件为系统自动发送，请勿回复！',
    'modify_due': '尊敬的{0}：\n\n您投稿的会议{1}即将到达修改稿投递截止日期，如果您想再次提交修改稿的话，请在{2}之前完成投稿。\n\n本邮件为系统自动发送，请勿回复！',
    'first_passed': '尊敬的{username}：\n\n您向会议{conference}投稿的论文{paper}，现经过会议主办方的评审，评审结果如下：'
                    '您的投稿ID{submission}已通过评审，主办方将予以录用。在该会议开放会议注册时，我们会再次发送邮件提醒您参会。'
                    '\n\n本邮件为系统自动发送，请勿回复！',
    'first_rejected': '尊敬的{username}：\n\n您向会议{conference}投稿的论文{paper}，现经过会议主办方的评审，评审结果如下：'
                      '您的投稿ID{submission}未能通过评审。\n评审意见如下：{}\n如您存在异议，请和会议主办方进行联系。'
                      '\n\n本邮件为系统自动发送，请勿回复！',
    'need_modified': '尊敬的{username}：\n\n您向会议{conference}投稿的论文{paper}，现经过会议主办方的评审，评审结果如下：'
                     '您的投稿ID{submission}暂未通过评审，但修改后主办方可能予以录用。\n评审意见如下：{}\n'
                     '请您根据评审意见进行修改，并在{modify_due}前完成修改稿提交。'
                     '\n\n本邮件为系统自动发送，请勿回复！',
    'modification_passed':  '尊敬的{username}：\n\n您向会议{conference}投稿的论文修改稿{paper}，现经过会议主办方的评审，评审结果如下：'
                            '您的投稿ID{submission}已通过评审，主办方将予以录用。在该会议开放会议注册时，我们会再次发送邮件提醒您参会。'
                            '\n\n本邮件为系统自动发送，请勿回复！',
    'modification_rejected':  '尊敬的{username}：\n\n您向会议{conference}投稿的论文修改稿{paper}，现经过会议主办方的评审，评审结果如下：'
                              '您的投稿ID{submission}未通过评审。\n评审意见如下：{}\n'
                              '如您存在异议，请和会议主办方进行联系。'
                              '\n\n本邮件为系统自动发送，请勿回复！',
}

FROM_EMAIL = 'demonsNearby@163.com'