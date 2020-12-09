import numpy as np

# 基本设定，暴击，冻结暴击，施法时间，冰指和冰智概率
critical = 1/3
critical_expectation = 1 + critical
critical_expectation = min(critical_expectation, 2)
freeze_critical_expectation = min(1 + 1.5 * critical + 0.5, 2)
freezeBolt_spellTime = 2
gcd = 1.5
fingersOfFrost_probability = 0.15
brainFreeze_probability = 0.3
print(freeze_critical_expectation)

#寒冰箭设定，基本伤害，期望伤害，冻结下期望伤害
frostBolt_basic_damage = 756
frostBolt_damage_expectation = frostBolt_basic_damage * critical_expectation
frostBolt_damage_freeze_expectation = frostBolt_basic_damage * freeze_critical_expectation

#冰枪设定，基本伤害，连锁反应天赋伤害，冰指下期望伤害
iceLance_basic_damage = 562
iceLance_chain_damage = iceLance_basic_damage * 1.15

iceLance_basic_damage_fingersOfFrost_expectation = iceLance_basic_damage * 3 * freeze_critical_expectation
iceLance_chain_damage_fingersOfFrost_expectation = iceLance_chain_damage * 3 * freeze_critical_expectation

#冰风暴设定，基本伤害，冰智下基础伤害，冰智下期望伤害
iceStorm_basic_damage = 1220
iceStorm_damage_brainFreeze = iceStorm_basic_damage * 1.5
iceStorm_damage_brainFreeze_expectation = iceStorm_damage_brainFreeze / 3 * critical_expectation \
                                          + iceStorm_damage_brainFreeze / 3 * 2 * freeze_critical_expectation

damage = 0
time = 0
fingersOfFrost_number = 0
brainFreeze_number = 0
#t = np.random.random()


#第一种打法，无论何时都是冰智优先，不管有没有冰指，只要有冰智都打1+1+2
while damage < 100000000000:
    #读条一个寒冰箭
    time = time + freezeBolt_spellTime
    damage = damage + frostBolt_damage_expectation
    fingersOfFrost_trigger = np.random.random()
    brainFreeze_trigger = np.random.random()
    #之前有冰指，没有触发冰智，读完这个寒冰箭打一个冰指的冰枪
    if fingersOfFrost_number > 0 and brainFreeze_number == 0:
        time = time + gcd
        damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
        fingersOfFrost_number -= 1
        #刚读完的寒冰箭触发了冰指，没触发冰智，扔掉所有之前存的冰指再扔了这个冰指，回去打寒冰箭
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            while fingersOfFrost_number > 0:
                time = time + gcd
                damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
                fingersOfFrost_number -= 1
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
        # 刚读完的寒冰箭触发了冰智，没触发冰指，改变资源数量后正常打1+1+2，等效于回到开头打寒冰箭
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭触发了冰智和冰指，改变资源数量后正常打1+1+2，等效于回到开头打寒冰箭
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            fingersOfFrost_number += 1
            fingersOfFrost_number = min(fingersOfFrost_number, 2)
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
    # 之前触发了冰智，没有触发冰指，正常1+1+2
    elif fingersOfFrost_number == 0 and brainFreeze_number == 1:
        time = time + gcd * 3
        damage = damage - frostBolt_damage_expectation + frostBolt_damage_freeze_expectation
        damage = damage + iceStorm_damage_brainFreeze_expectation + iceLance_chain_damage_fingersOfFrost_expectation * 2
        brainFreeze_number = 0
        #刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发了冰指，没触发冰智，浪费一个冰指
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            pass
        # 刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发冰智，没触发冰指，多了一个冰智
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发了冰指和冰智，浪费一个冰指，多了一个冰智
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)

    #  之前触发了冰智和冰指，浪费掉存的冰指正常1+1+2
    elif fingersOfFrost_number > 0 and brainFreeze_number == 1:
        time = time + gcd * 3
        damage = damage - frostBolt_damage_expectation + frostBolt_damage_freeze_expectation
        damage = damage + iceStorm_damage_brainFreeze_expectation + iceLance_chain_damage_fingersOfFrost_expectation * 2
        brainFreeze_number = 0
        fingersOfFrost_number = 0
        #刚读完的寒冰箭在前一个寒冰箭冰智对应的冰风暴出手后，触发了冰指，没触发冰智，浪费一个冰指
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            pass
        # 刚读完的寒冰箭在前一个寒冰箭冰智对应的冰风暴出手后，触发冰智，没触发冰指，多了一个冰智
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭在前一个寒冰箭冰智对应的冰风暴出手后，触发了冰指和冰智，浪费一个冰指，多了一个冰智
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
    #之前啥都没，读完这个寒冰箭计算完触发，回头继续读
    else:
        # 刚读完的寒冰箭，触发了冰指冰智
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            fingersOfFrost_number += 1
            fingersOfFrost_number = min(fingersOfFrost_number, 2)
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭，触发冰智，没触发冰指
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭触发了冰指没触发冰智
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            fingersOfFrost_number += 1
            fingersOfFrost_number = min(fingersOfFrost_number, 2)

dps_1 = damage / time


damage = 0
time = 0
fingersOfFrost_number = 0
brainFreeze_number = 0

#第二种打法，绝不浪费任意可以打出的冰指，有冰智和冰指也先打冰指对应的冰枪再去1+1+2
while damage < 100000000000:
    #读条一个寒冰箭
    time = time + freezeBolt_spellTime
    damage = damage + frostBolt_damage_expectation
    fingersOfFrost_trigger = np.random.random()
    brainFreeze_trigger = np.random.random()
    #之前触发了冰指，没有触发冰智，扔完所有存的冰指
    if fingersOfFrost_number > 0 and brainFreeze_number == 0:
        while fingersOfFrost_number > 0:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
            fingersOfFrost_number -= 1
        #刚读完的寒冰箭触发了冰指，没触发冰智，扔完之前存的冰指对应的冰枪，立刻扔掉这个寒冰箭冰指的冰枪，回头读寒冰箭
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
        # 刚读完的寒冰箭触发了冰智，没触发冰指，扔完之前存的冰指对应的冰枪，回去正常打1+1+2，
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭触发了冰智和冰指，扔完之前存的冰指对应的冰枪，先扔这个寒冰箭冰指对应的冰枪，再回到开头打1+1+2
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
    # 之前触发了冰智，没有触发冰指，正常1+1+2
    elif fingersOfFrost_number == 0 and brainFreeze_number == 1:
        time = time + gcd * 3
        damage = damage - frostBolt_damage_expectation + frostBolt_damage_freeze_expectation
        damage = damage + iceStorm_damage_brainFreeze_expectation + iceLance_chain_damage_fingersOfFrost_expectation * 2
        brainFreeze_number = 0
        #刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发了冰指，没触发冰智，浪费一个冰指
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            pass
        # 刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发冰智，没触发冰指，多了一个冰智
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发了冰指和冰智，浪费一个冰指，多了一个冰智
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
    #  之前触发了冰智和冰指，扔完之前存的冰枪，看这个寒冰箭有没有触发冰指，再回头打1+1+2
    elif fingersOfFrost_number > 0 and brainFreeze_number == 1:
        while fingersOfFrost_number > 0:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
            fingersOfFrost_number -= 1
        #刚读完的寒冰箭在之前冰指对应的冰枪出手后，触发了冰指，没触发冰智，打完所有存的冰指，打出这个寒冰箭冰指的冰枪，回头1+1+2
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
        # 刚读完的寒冰箭之前存的冰指对应的冰枪出手后，触发冰智，没触发冰指，前一个冰智还在，浪费一个冰智
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            pass
        # 刚读完的寒冰箭在之前冰指对应的冰枪出手后，触发了冰指和冰智，前一个冰智还在,浪费一个冰智，打出这个寒冰箭冰指对应的冰枪，回头
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
    #之前啥都没有，读完这个寒冰箭计算完触发，回头继续读
    else:
        # 刚读完的寒冰箭，触发了冰指冰智
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            fingersOfFrost_number += 1
            fingersOfFrost_number = min(fingersOfFrost_number, 2)
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭，触发冰智，没触发冰指
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭触发了冰指没触发冰智
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            fingersOfFrost_number += 1
            fingersOfFrost_number = min(fingersOfFrost_number, 2)

dps_2 = damage / time

damage = 0
time = 0
fingersOfFrost_number = 0
brainFreeze_number = 0

#第三种打法，不浪费任何冰指，同时除非是之前只有冰智，并且刚扔出去了寒冰箭，才打1+1+2，否则有冰智直接打冰风暴+2冰枪
while damage < 100000000000:
    #读条一个寒冰箭
    time = time + freezeBolt_spellTime
    damage = damage + frostBolt_damage_expectation
    fingersOfFrost_trigger = np.random.random()
    brainFreeze_trigger = np.random.random()
    #之前触发了冰指，没有触发冰智，打完所有存的冰指
    if fingersOfFrost_number > 0 and brainFreeze_number == 0:
        while fingersOfFrost_number > 0:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
            fingersOfFrost_number -= 1
        # 刚读完的寒冰箭触发了冰指，没触发冰智，扔完之前冰指对应的冰枪立刻扔掉这个寒冰箭冰指的冰枪，回去打寒冰箭
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
        # 刚读完的寒冰箭触发了冰智，没触发冰指，扔完之前冰指对应的冰枪，打这个冰智的冰风暴+2冰枪
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd * 3
            damage = damage + iceStorm_damage_brainFreeze_expectation + \
                     iceLance_chain_damage_fingersOfFrost_expectation * 2
            brainFreeze_number = 0
        # 刚读完的寒冰箭触发了冰智和冰指，扔完之前冰指对应的冰枪，先扔这个寒冰箭冰指对应的冰枪，再打这个冰智的冰风暴+2冰枪
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
            time = time + gcd * 3
            damage = damage + iceStorm_damage_brainFreeze_expectation + iceLance_chain_damage_fingersOfFrost_expectation * 2
            brainFreeze_number = 0
    # 之前触发了冰智，没有触发冰指，正常1+1+2
    elif fingersOfFrost_number == 0 and brainFreeze_number == 1:
        time = time + gcd * 3
        damage = damage - frostBolt_damage_expectation + frostBolt_damage_freeze_expectation
        damage = damage + iceStorm_damage_brainFreeze_expectation + iceLance_chain_damage_fingersOfFrost_expectation * 2
        brainFreeze_number = 0
        # 刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发了冰指，没触发冰智，浪费一个冰指
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            pass
        # 刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发冰智，没触发冰指，多了一个冰智,打完这个1+1+2，直接打这个冰智的冰风暴+2冰枪
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd * 3
            damage = damage + iceStorm_damage_brainFreeze_expectation + \
                     iceLance_chain_damage_fingersOfFrost_expectation * 2
        # 刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发了冰指和冰智，浪费一个冰指，多了一个冰智,打完这个1+1+2，
        # 直接打这个冰智的冰风暴+2冰枪
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd * 3
            damage = damage + iceStorm_damage_brainFreeze_expectation + \
                     iceLance_chain_damage_fingersOfFrost_expectation * 2
    #  之前触发了冰智和冰指，读完这个寒冰箭，扔完所有冰指打之前冰智的冰风暴+2冰枪
    elif fingersOfFrost_number > 0 and brainFreeze_number == 1:
        while fingersOfFrost_number > 0:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
            fingersOfFrost_number -= 1
        time = time + gcd * 3
        damage = damage + iceStorm_damage_brainFreeze_expectation + iceLance_chain_damage_fingersOfFrost_expectation * 2
        brainFreeze_number = 0
        #刚读完的寒冰箭触发了冰指，没触发冰智，扔完之前的冰指冰智，立刻扔掉这个寒冰箭冰指的冰枪，回去打寒冰箭
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
        # 刚读完的寒冰箭触发了冰智，没触发冰指，浪费一个冰智，扔完之前的冰指冰智,回头
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            pass
        # 刚读完的寒冰箭触发了冰智和冰指，浪费一个冰智，扔完之前冰指对应的冰枪，立刻扔掉这个寒冰箭冰指的冰枪，回头
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
    else:
        # 刚读完的寒冰箭，触发了冰指冰智
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            fingersOfFrost_number += 1
            fingersOfFrost_number = min(fingersOfFrost_number, 2)
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭，触发冰智，没触发冰指
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭触发了冰指没触发冰智
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            fingersOfFrost_number += 1
            fingersOfFrost_number = min(fingersOfFrost_number, 2)


dps_3 = damage / time

damage = 0
time = 0
fingersOfFrost_number = 0
brainFreeze_number = 0

#第四种打法，除非刚好读完一个寒冰箭同时有冰智，否则不打1+1+2，直接打冰风暴+2冰枪，同时有冰智冰指，冰智优先，即浪费掉冰指（定性也能分析出这个不行）
while damage < 100000000000:
    #读条一个寒冰箭
    time = time + freezeBolt_spellTime
    damage = damage + frostBolt_damage_expectation
    fingersOfFrost_trigger = np.random.random()
    brainFreeze_trigger = np.random.random()
    #之前有冰指，没有触发冰智，读完这个寒冰箭打一个冰指的冰枪
    if fingersOfFrost_number > 0 and brainFreeze_number == 0:
        time = time + gcd
        damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
        fingersOfFrost_number -= 1
        #刚读完的寒冰箭触发了冰指，没触发冰智，扔掉所有之前存的冰指再扔了这个冰指，回去打寒冰箭
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            while fingersOfFrost_number > 0:
                time = time + gcd
                damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
                fingersOfFrost_number -= 1
            time = time + gcd
            damage = damage + iceLance_chain_damage_fingersOfFrost_expectation
        # 刚读完的寒冰箭触发了冰智，没触发冰指，打冰风暴+2冰枪，可能浪费冰指
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd * 3
            damage = damage + iceStorm_damage_brainFreeze_expectation + \
                     iceLance_chain_damage_fingersOfFrost_expectation * 2
            fingersOfFrost_number = 0
        # 刚读完的寒冰箭触发了冰智和冰指，打冰风暴+2冰枪，起码浪费1冰指
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd * 3
            damage = damage + iceStorm_damage_brainFreeze_expectation + \
                     iceLance_chain_damage_fingersOfFrost_expectation * 2
            fingersOfFrost_number = 0
    # 之前触发了冰智，没有触发冰指，正常1+1+2
    elif fingersOfFrost_number == 0 and brainFreeze_number == 1:
        time = time + gcd * 3
        damage = damage - frostBolt_damage_expectation + frostBolt_damage_freeze_expectation
        damage = damage + iceStorm_damage_brainFreeze_expectation + \
                 iceLance_chain_damage_fingersOfFrost_expectation * 2
        brainFreeze_number = 0
        #刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发了冰指，没触发冰智，浪费一个冰指
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            pass
        # 刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发冰智，没触发冰指，打完之前冰智的1+1+2，打这个冰智的冰风暴+2冰枪
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd * 3
            damage = damage + iceStorm_damage_brainFreeze_expectation + \
                     iceLance_chain_damage_fingersOfFrost_expectation * 2
        # 刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发了冰指和冰智，打完之前冰智的1+1+2，打这个冰智的冰风暴+2冰枪，浪费一个冰指
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd * 3
            damage = damage + iceStorm_damage_brainFreeze_expectation + \
                     iceLance_chain_damage_fingersOfFrost_expectation * 2

    #  之前触发了冰智和冰指，浪费掉存的冰指正常1+1+2
    elif fingersOfFrost_number > 0 and brainFreeze_number == 1:
        time = time + gcd * 3
        damage = damage - frostBolt_damage_expectation + frostBolt_damage_freeze_expectation
        damage = damage + iceStorm_damage_brainFreeze_expectation + iceLance_chain_damage_fingersOfFrost_expectation * 2
        brainFreeze_number = 0
        fingersOfFrost_number = 0
        #刚读完的寒冰箭之前冰智对应的冰风暴出手后，触发了冰指，没触发冰智，浪费一个冰指
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            pass
        # 刚读完的寒冰箭在之前冰智对应的冰风暴出手后，触发冰智，没触发冰指，打冰风暴+2冰枪
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd * 3
            damage = damage + iceStorm_damage_brainFreeze_expectation + \
                     iceLance_chain_damage_fingersOfFrost_expectation * 2
        # 刚读完的寒冰箭在前一个寒冰箭冰智对应的冰风暴出手后，触发了冰指和冰智，浪费一个冰指，打冰风暴+2冰枪
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            time = time + gcd * 3
            damage = damage + iceStorm_damage_brainFreeze_expectation + \
                     iceLance_chain_damage_fingersOfFrost_expectation * 2
    #之前啥都没，读完这个寒冰箭计算完触发，回头继续读
    else:
        # 刚读完的寒冰箭，触发了冰指冰智
        if fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            fingersOfFrost_number += 1
            fingersOfFrost_number = min(fingersOfFrost_number, 2)
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭，触发冰智，没触发冰指
        elif fingersOfFrost_trigger > fingersOfFrost_probability and brainFreeze_trigger <= brainFreeze_probability:
            brainFreeze_number += 1
            brainFreeze_number = min(brainFreeze_number, 1)
        # 刚读完的寒冰箭触发了冰指没触发冰智
        elif fingersOfFrost_trigger <= fingersOfFrost_probability and brainFreeze_trigger > brainFreeze_probability:
            fingersOfFrost_number += 1
            fingersOfFrost_number = min(fingersOfFrost_number, 2)

dps_4 = damage / time


print(dps_1)
print(dps_2)
print(dps_3)
print(dps_4)