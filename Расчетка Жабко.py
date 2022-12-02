# Менять значения необходимо только в этом блоке
#
# После заполнения всех пунктов необходимо нажать "Среда выполнения" ->
# -> "Выполнить все" (Сtrl + F9)
#
# Результат находится в файле report.tex (сбоку иконка с папкой),
# его содержимое необходимо поместить в проект, который нужно создать
# на overleaf.com или в любом другом онлайн компиляторе LATEX


year = '2022'
tutor = 'Жабко Г.П.'
student = 'Кулик Д.Д.'
group = '4941101/10301'
variant = '8'

f = 9e9

angleOfIncidence = 70

firstMaterial = 'медь'
secondMaterial = 'поликор'
thirdMaterial = 'железо'

d1 = 0.3e-6
d2 = 1e-3
d3 = 0.1e-6

polarization = 'паралл'


import pylatex
from math import pi
from scipy.constants import epsilon_0
from scipy.constants import speed_of_light
from cmath import cos
from cmath import sqrt
from cmath import exp
from cmath import sin
from math import log10#@title
from pylatex import NewLine
from pylatex import NoEscape
from pylatex import Math

geometry_options = {'top': '2cm', 'bottom': '2cm', 'left': '2cm', 'right': '2cm', 'bindingoffset': '0cm'}
doc = pylatex.Document(geometry_options=geometry_options, fontenc='T1, T2A', font_size='large')
doc.preamble.append(pylatex.Command('linespread', '1.3'))
doc.packages.append(pylatex.Package('babel', options=['english', 'bulgarian', 'ukrainian', 'russian']))
doc.packages.append(pylatex.Package('physics'))

title = r'''
\begin{titlepage}%

\begin{center}%

\large Санкт-Петербургский Политехнический Университет Петра Великого \\
\large Институт электроники и телекоммуникаций \\
\large Высшая школа прикладной физики и космических технологий \\[6cm]

\huge Отчёт по расчётному заданию \\[0.5cm] % название работы, затем отступ 0,5см
\large Вариант №''' + variant + r''' \\[5.1cm]
% \large Тема работы\\[5cm]

\end{center}


\begin{flushright} % выравнивание по правому краю
\begin{minipage}{0.25\textwidth} % врезка в половину ширины текста
\begin{flushleft} % выровнять её содержимое по левому краю

\large\textbf{Работу выполнила:}\\
\large''' + student + r'''\\
\large {Группа:} \\
\large''' + group + r'''
\large \textbf{Преподаватель:}\\
\large ''' + tutor + r'''

\end{flushleft}
\end{minipage}
\end{flushright}

\vfill % заполнить всё доступное ниже пространство

\begin{center}
\large Санкт-Петербург \\
\large ''' + year + r''' % вывести дату
\end{center} % закончить выравнивание по центру

\end{titlepage} % конец титульной страницы

\vfill % заполнить всё доступное ниже пространство
'''
doc.append(NoEscape(title))
d = {firstMaterial: d1, secondMaterial: d2, thirdMaterial: d3}
with doc.create(pylatex.Section('Исходные данные')):
    doc.append('Частота =' + str(f) + ' Гц\n')
    doc.append(pylatex.Math(data=['\\theta=', str(angleOfIncidence), '^\\circ'], inline=True, escape=False))
    doc.append('\nПервый слой - ' + firstMaterial + ', толщина - ' + str(d1) + ' м')
    doc.append('\nВторой слой - ' + secondMaterial + ', толщина - ' + str(d2) + ' м')
    doc.append('\nТретий слой - ' + thirdMaterial + ', толщина - ' + str(d3) + ' м')
    doc.append('\nПоляризация - ' + polarization)
with doc.create(pylatex.Section('Расчёты:')):
    materials = [firstMaterial, secondMaterial, thirdMaterial]
    omega = 2 * pi * f
    angleOfIncidence *= pi / 180

    relativeDielectricConstants = {'полиэтилен': 2.4,
                                   'полистирол': 2.5,
                                   'фторопласт': 2.2,
                                   'ситал': 10,
                                   'поликор': 9.5,
                                   'гитенакс': 6,
                                   'бумага': 2.2}

    typicalDielectricLosses = {'полиэтилен': 0.00045,
                               'полистирол': 0.00035,
                               'фторопласт': 0.00025,
                               'ситал': 0.00035,
                               'поликор': 0.00003,
                               'гитенакс': 0.02,
                               'бумага': 0.01}

    conductivityOfMetals = {'серебро': 66e6,
                            'медь': 59e6,
                            'алюминий': 38e6,
                            'латунь': 16e6,
                            'железо': 12e6}

    freeSpacePropagationConstant = omega / speed_of_light
    j = complex(0, 1)

    doc.append(Math(data=['\\omega=2*\\pi*f=', omega], escape=False, inline=True))
    doc.append(NewLine())
    doc.append(Math(data=['k=', freeSpacePropagationConstant], inline=True))
    doc.append(NewLine())

    # complexDielectricConstant - обозначается как эпсилон с индексом r
    # relativePermeability - обозначается как мю с индексом r

    complexDielectricConstants = dict()
    relativePermeabilitys = dict()
    propagationConstantInScreenMaterials = dict()
    fresnelCoefficients = dict()
    K = dict()
    G = dict()

    for material in materials:
        layer_number = str(materials.index(material) + 1)

        doc.append(NewLine())
        doc.append(layer_number + '-й слой:')

        if material == 'железо':
            relativePermeability = 400
        else:
            relativePermeability = 1

        doc.append(NewLine())
        doc.append(Math(data=['\\mu_{r' + layer_number + '}=', relativePermeability], escape=False, inline=True))
        doc.append(NewLine())

        relativePermeabilitys[material] = relativePermeability
        # imaginePartOfDielectricConstant - обозначается в формулах как эпсилон два штриха
        # realPartOfDielectricConstant - обозначается в формулах как эпсилон штрих

        if material in conductivityOfMetals:
            imaginePartDielectricConst = conductivityOfMetals.get(material) / (omega * epsilon_0)
            realPartOfDielectricConstant = 1
        else:
            imaginePartDielectricConst = relativeDielectricConstants.get(material) * \
                                         typicalDielectricLosses.get(material)
            realPartOfDielectricConstant = relativeDielectricConstants.get(material)
        complexDielectricConstant = complex(realPartOfDielectricConstant, - imaginePartDielectricConst)

        doc.append(Math(data=['\\varepsilon\'_' + layer_number + '=', realPartOfDielectricConstant],
                        escape=False, inline=True))
        doc.append(NewLine())
        doc.append(Math(data=['\\varepsilon\'\'_' + layer_number + '=', imaginePartDielectricConst],
                        escape=False, inline=True))
        doc.append(NewLine())
        doc.append(Math(data=[
            '\\varepsilon_{r' + layer_number + '}=\\varepsilon\'_' + layer_number + ' - i\\varepsilon\'\'_' +
            layer_number + '=',
            complexDielectricConstant],
            escape=False, inline=True))
        doc.append(NewLine())

        # propagationConstantInScreenMaterial - обозначается как гамма

        propagationConstantInScreenMaterial = freeSpacePropagationConstant * sqrt(
            complexDielectricConstant * relativePermeabilitys.get(material) - sin(angleOfIncidence) ** 2)
        propagationConstantInScreenMaterials[material] = propagationConstantInScreenMaterial

        doc.append(Math(
            data=['\\gamma_' + layer_number + '=k\\sqrt{\\varepsilon_{r' + layer_number + '}\\mu_{r' + layer_number +
                  '} - \\sin ^ 2{\\theta}}=',
                  propagationConstantInScreenMaterial], escape=False, inline=True))
        doc.append(NewLine())

        fresnelCoefficient = 0
        if polarization == 'перпен':
            fresnelCoefficient = (freeSpacePropagationConstant * relativePermeability * cos(
                angleOfIncidence) - propagationConstantInScreenMaterial) / (
                                         freeSpacePropagationConstant * relativePermeability * cos(angleOfIncidence) +
                                         propagationConstantInScreenMaterial)

            doc.append(Math(data=['R_' + layer_number +
                                  '=\\frac{k\\mu_r\\cos\\theta-\\gamma}{k\\mu_r\\cos\\theta+\\gamma}=',
                                  fresnelCoefficient],escape=False, inline=True))

        elif polarization == 'паралл':
            fresnelCoefficient = (freeSpacePropagationConstant * complexDielectricConstant * cos(
                angleOfIncidence) - propagationConstantInScreenMaterial) / (freeSpacePropagationConstant *
                                                                            complexDielectricConstant *
                                                                            cos(angleOfIncidence) +
                                                                            propagationConstantInScreenMaterial)

            doc.append(Math(data=[
                'R_' + layer_number + '=\\frac{k\\varepsilon_{r' + layer_number + '}\\cos\\theta-\\gamma_' +
                layer_number + '}{k\\varepsilon_{r' + layer_number + '}\\cos\\theta+\\gamma_' + layer_number + '}=',
                fresnelCoefficient], escape=False, inline=True))
            doc.append(NewLine())

        fresnelCoefficients[material] = fresnelCoefficient

        screeningFactor = (1 - fresnelCoefficient ** 2) * exp(
            -j * propagationConstantInScreenMaterial * d.get(material)) / (1 - fresnelCoefficient ** 2 * exp(
            -j * 2 * propagationConstantInScreenMaterial * d.get(material)))
        K[material] = screeningFactor
        doc.append(
            Math(data=[
                'K_' + layer_number + '=\\frac{(1 - R_' + layer_number + ' ^ 2) \\exp(-i \\gamma_' + layer_number +
                ' d_' + layer_number + ')}{(1 - R_' + layer_number + ' ^ 2 \\exp(-i 2 \\gamma_' + layer_number +
                ' d_' + layer_number + '))}=',
                screeningFactor],
                escape=False, inline=True))
        doc.append(NewLine())
        doc.append(Math(data=['\\abs{K_' + layer_number + '}=', abs(screeningFactor)], inline=True, escape=False))
        doc.append(NewLine())

        reflectionCoefficient = fresnelCoefficient * \
                                (1 - exp(-j * 2 * propagationConstantInScreenMaterial * d.get(material))) / \
                                (1 - fresnelCoefficient ** 2 * exp(-j * 2 * propagationConstantInScreenMaterial *
                                                                   d.get(material)))
        G[material] = reflectionCoefficient

        doc.append(
            Math(data=[
                'G_' + layer_number + ' = \\frac{R_' + layer_number + ' (1 - \\exp(-j 2 \\gamma_' + layer_number +
                ' d_' + layer_number + '))}{(1 - R' + layer_number + ' ^ 2 \\exp(-j 2 \\gamma_' + layer_number + ' d_' +
                layer_number + '))}=',
                reflectionCoefficient],
                inline=True, escape=False))
        doc.append(NewLine())
        doc.append(Math(data=['\\abs{G_' + layer_number + '}=', abs(reflectionCoefficient)], inline=True, escape=False))
        doc.append(NewLine())

    K1 = K.get(firstMaterial)
    K2 = K.get(secondMaterial)
    K3 = K.get(thirdMaterial)

    G1 = G.get(firstMaterial)
    G2 = G.get(secondMaterial)
    G3 = G.get(thirdMaterial)

    doc.append(NewLine())
    doc.append('Многолослойный экран')
    doc.append(NewLine())

    K12 = (K1 * K2) / (1 - G1 * G2)
    K21 = K12

    doc.append(Math(data=['K_{12}=K_{21}=\\frac{K_1 K_2}{1 - G_1 G_2}=', K12], inline=True, escape=False))
    doc.append(NewLine())

    K13 = (K1 * K3) / (1 - G1 * G3)
    K31 = K13

    doc.append(Math(data=['K_{13} = K_{31} =  \\frac{K_1 K_3}{1 - G_1 G_3}=', K13], inline=True, escape=False))
    doc.append(NewLine())

    K23 = (K2 * K3) / (1 - G2 * G3)
    K32 = K23

    doc.append(Math(data=['K_{23} = K_{32} =  \\frac{K_2 K_3}{1 - G_2 G_3}=', K23], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(NewLine())

    G12 = G1 + (K1 ** 2 * G2) / (1 - G1 * G2)
    doc.append(Math(data=['G_{12}=G_1 + \\frac{K_1 ^ 2 G_2}{1 - G_1 G_2}=', G12], inline=True, escape=False))
    doc.append(NewLine())

    G21 = G2 + (K2 ** 2 * G1) / (1 - G1 * G2)
    doc.append(Math(data=['G_{21} = G_2 + \\frac{K_2 ^ 2 G_1}{1 - G_1 G_2}=', G21], inline=True, escape=False))
    doc.append(NewLine())

    G13 = G1 + (K1 ** 2 * G3) / (1 - G1 * G3)
    doc.append(Math(data=['G_{13}=G_1 + \\frac{K_1 ^ 2 G_3}{1 - G_1 G_3}=', G13], inline=True, escape=False))
    doc.append(NewLine())

    G31 = G3 + (K3 ** 2 * G1) / (1 - G1 * G3)
    doc.append(Math(data=['G_{31} = G_3 + \\frac{K_3 ^ 2 G_1}{1 - G_1 G_3}=', G31], inline=True, escape=False))
    doc.append(NewLine())

    G23 = G2 + (K2 ** 2 * G3) / (1 - G2 * G3)
    doc.append(Math(data=['G_{23}=G_2 + \\frac{K_2 ^ 2 G_3}{1 - G_2 G_3}=', G23], inline=True, escape=False))
    doc.append(NewLine())

    G32 = G3 + (K3 ** 2 * G2) / (1 - G2 * G3)
    doc.append(Math(data=['G_{32} = G_3 + \\frac{K_3 ^ 2 G_2}{1 - G_2 G_3}=', G32], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(NewLine())

    K123 = (K12 * K3) / (1 - G3 * G21)
    doc.append(Math(data=['K_{123}=\\frac{K_{12} K_3}{1 - G_3  G_{21}}=', K123], inline=True, escape=False))
    doc.append(NewLine())

    K132 = (K13 * K2) / (1 - G2 * G31)
    doc.append(Math(data=['K_{132}=\\frac{K_{13} K_2}{1 - G_2  G_{31}}=', K132], inline=True, escape=False))
    doc.append(NewLine())

    K213 = (K21 * K3) / (1 - G3 * G12)
    doc.append(Math(data=['K_{213}=\\frac{K_{21} K_3}{1 - G_3  G_{12}}=', K213], inline=True, escape=False))
    doc.append(NewLine())

    K231 = (K23 * K1) / (1 - G1 * G32)
    doc.append(Math(data=['K_{231}=\\frac{K_{23} K_1}{1 - G_1  G_{32}}=', K231], inline=True, escape=False))
    doc.append(NewLine())

    K312 = (K31 * K2) / (1 - G2 * G13)
    doc.append(Math(data=['K_{312}=\\frac{K_{31} K_2}{1 - G_2  G_{13}}=', K312], inline=True, escape=False))
    doc.append(NewLine())

    K321 = (K32 * K1) / (1 - G1 * G23)
    doc.append(Math(data=['K_{321}=\\frac{K_{32} K_1}{1 - G_1  G_{23}}=', K321], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(NewLine())

    G123 = G12 + (G3 * K12 ** 2) / (1 - G3 * G21)
    doc.append(Math(data=['G_{123}=G_{12} + \\frac{G_3 K_{12} ^ 2}{1 - G_3 G_{21}}=', G123], inline=True, escape=False))
    doc.append(NewLine())

    G132 = G13 + (G2 * K13 ** 2) / (1 - G2 * G31)
    doc.append(Math(data=['G_{132}=G_{13} + \\frac{G_2 K_{13} ^ 2}{1 - G_2 G_{31}}=', G132], inline=True, escape=False))
    doc.append(NewLine())

    G213 = G21 + (G3 * K21 ** 2) / (1 - G3 * G12)
    doc.append(Math(data=['G_{213}=G_{21} + \\frac{G_3 K_{21} ^ 2}{1 - G_3 G_{12}}=', G213], inline=True, escape=False))
    doc.append(NewLine())

    G231 = G23 + (G1 * K23 ** 2) / (1 - G1 * G32)
    doc.append(Math(data=['G_{231}=G_{23} + \\frac{G_1 K_{23} ^ 2}{1 - G_1 G_{32}}=', G231], inline=True, escape=False))
    doc.append(NewLine())

    G312 = G31 + (G2 * K31 ** 2) / (1 - G2 * G13)
    doc.append(Math(data=['G_{312}=G_{31} + \\frac{G_2 K_{31} ^ 2}{1 - G_2 G_{13}}=', G312], inline=True, escape=False))
    doc.append(NewLine())

    G321 = G32 + (G1 * K32 ** 2) / (1 - G1 * G23)
    doc.append(Math(data=['G_{321}=G_{32} + \\frac{G_1 K_{32} ^ 2}{1 - G_1 G_{23}}=', G321], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(NewLine())

    KForChoice = dict()
    KForChoice[abs(K123)] = '123'
    doc.append(Math(data=['\\abs{K_{123}}= ', abs(K123)], inline=True, escape=False))
    doc.append(NewLine())
    KForChoice[abs(K132)] = '132'
    doc.append(Math(data=['\\abs{K_{132}}= ', abs(K132)], inline=True, escape=False))
    doc.append(NewLine())
    KForChoice[abs(K213)] = '213'
    doc.append(Math(data=['\\abs{K_{213}}= ', abs(K213)], inline=True, escape=False))
    doc.append(NewLine())
    KForChoice[abs(K231)] = '231'
    doc.append(Math(data=['\\abs{K_{231}}= ', abs(K231)], inline=True, escape=False))
    doc.append(NewLine())
    KForChoice[abs(K312)] = '312'
    doc.append(Math(data=['\\abs{K_{312}}= ', abs(K312)], inline=True, escape=False))
    doc.append(NewLine())
    KForChoice[abs(K321)] = '321'
    doc.append(Math(data=['\\abs{K_{321}}= ', abs(K321)], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(NewLine())

    doc.append(Math(data=['\\abs{G_{123}}= ', abs(G123)], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(Math(data=['\\abs{G_{132}}= ', abs(G132)], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(Math(data=['\\abs{G_{213}}= ', abs(G213)], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(Math(data=['\\abs{G_{231}}= ', abs(G231)], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(Math(data=['\\abs{G_{312}}= ', abs(G312)], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(Math(data=['\\abs{G_{321}}= ', abs(G321)], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(NewLine())

    doc.append('Исходя из полученных значений коэффициентов отражения оптимальный порядок слоев:')
    with doc.create(pylatex.Enumerate()) as enum:
        enum.add_item(materials[int(KForChoice.get(max(KForChoice))[0]) - 1])
        enum.add_item(materials[int(KForChoice.get(max(KForChoice))[1]) - 1])
        enum.add_item(materials[int(KForChoice.get(max(KForChoice))[2]) - 1])

    A123 = 20 * log10(abs(K123))
    A132 = 20 * log10(abs(K132))
    A213 = 20 * log10(abs(K213))
    A231 = 20 * log10(abs(K231))
    A312 = 20 * log10(abs(K312))
    A321 = 20 * log10(abs(K321))

    doc.append(Math(data=['A_{123} = 20 \\log_{10}\\abs{K_{123}}=', A123], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(Math(data=['A_{132} = 20 \\log_{10}\\abs{K_{132}}=', A132], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(Math(data=['A_{213} = 20 \\log_{10}\\abs{K_{213}}=', A213], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(Math(data=['A_{231} = 20 \\log_{10}\\abs{K_{231}}=', A231], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(Math(data=['A_{312} = 20 \\log_{10}\\abs{K_{312}}=', A312], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(Math(data=['A_{321} = 20 \\log_{10}\\abs{K_{321}}=', A321], inline=True, escape=False))
    doc.append(NewLine())
    doc.append(NewLine())

    AForChoice = {A123: '123',
                  A132: '132',
                  A213: '213',
                  A231: '231',
                  A312: '312',
                  A321: '321'}

    doc.append('Исходя из полученных значений эффективности экранирования оптимальный порядок слоев:')
    with doc.create(pylatex.Enumerate()) as enum:
        enum.add_item(materials[int(AForChoice.get(max(AForChoice))[0]) - 1])
        enum.add_item(materials[int(AForChoice.get(max(AForChoice))[1]) - 1])
        enum.add_item(materials[int(AForChoice.get(max(AForChoice))[2]) - 1])

doc.generate_tex('reportKulikV8')
