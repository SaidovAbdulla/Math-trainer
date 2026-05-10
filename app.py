import streamlit as st
import random

# --- Инициализация памяти ---
if 'step' not in st.session_state:
    st.session_state.step, st.session_state.score = 0, 0
    st.session_state.current_ex = None
    st.session_state.game_over = False
    st.session_state.answered = False
    st.session_state.feedback = ""

# --- НАСТРОЙКА ЗАГОЛОВКА ---
st.set_page_config(page_title="Brain Gum", page_icon="🧠")
st.title("🧠 Brain Gum 🧠")

# --- Настройки в Sidebar ---
with st.sidebar:
    st.header("🛠 Настройки")
    
    mode = st.selectbox("Сложность (разрядность):", [
        "😄 Легкий уровень", 
        "😓 Средний уровень", 
        "😡 Продвинутый уровень", 
        "🎢 Хаос-режим (Рандом)"
    ])
    
    mode_to_digits = {
        "😄 Легкий уровень": 1,
        "😓 Средний уровень": 2,
        "😡 Продвинутый уровень": 3
    }
    
    op_choice = st.selectbox("Операция:", ["+", "-", "*", "/", "🎲 Вперемешку"])
    total_count = st.number_input("Количество задач:", 1, 50, 5)
    
    if st.button("🔌 Перезапуск"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- Функция генерации ---
def generate_problem(selected_mode, selected_op):
    if selected_mode == "🎢 Хаос-режим (Рандом)":
        d = random.randint(1, 3)
    else:
        d = mode_to_digits[selected_mode]
    
    op = random.choice(["+", "-", "*", "/"]) if selected_op == "🎲 Вперемешку" else selected_op

    low, high = 10**(d-1), (10**d) - 1
    
    if op == "+": a, b = random.randint(low, high), random.randint(low, high); res = a + b
    elif op == "-": a = random.randint(low, high); b = random.randint(low, a); res = a - b
    elif op == "*": a, b = random.randint(low, high), random.randint(1, 10); res = a * b
    else: res = random.randint(low, high); b = random.randint(2, 9); a = res * b
    
    vals = [a, b, res]
    mask_idx = random.randint(0, 2)
    correct = vals[mask_idx]
    
    display = [str(v) for v in vals]
    display[mask_idx] = "❓"
    
    problem_str = f"{display[0]} {op} {display[1]} = {display[2]}"
    
    return problem_str, correct

# --- Игровой процесс ---
if not st.session_state.game_over:
    if st.session_state.step < total_count:
        # Прогресс-бар
        st.progress(st.session_state.step / total_count)
        
        if st.session_state.current_ex is None:
            st.session_state.current_ex = generate_problem(mode, op_choice)
            st.session_state.answered = False
        
        txt, correct_ans = st.session_state.current_ex
        st.write(f"### 📋 Задание {st.session_state.step + 1} из {total_count}")
        st.info(f"## {txt}")

        if not st.session_state.answered:
            with st.form(key=f"form_{st.session_state.step}"):
                # Используем text_input БЕЗ кнопок +/-
                user_input = st.text_input("Введи число:", value="", placeholder="Пиши ответ здесь...")
                
                if st.form_submit_button("Подтвердить ⚡"):
                    # Проверка на число (учитывая возможный минус)
                    clean_input = user_input.strip()
                    if clean_input.lstrip('-').isdigit():
                        user_val = int(clean_input)
                        st.session_state.answered = True
                        if user_val == correct_ans:
                            st.session_state.score += 1
                            st.session_state.feedback = "✅ **Верно!** Отличная работа! 🎯"
                        else:
                            st.session_state.feedback = f"❌ **Неверно.** Правильный ответ: {correct_ans} 🙈"
                        st.rerun()
                    elif clean_input == "":
                        st.warning("⚠️ Сначала напиши ответ!")
                    else:
                        st.error("🔢 Вводить можно только цифры!")
        else:
            st.markdown(f"### {st.session_state.feedback}")
            if st.button("Дальше ⏭️"):
                st.session_state.step += 1
                st.session_state.current_ex = None
                st.rerun()
    else:
        st.session_state.game_over = True
        st.rerun()

# --- Финал ---
else:
    st.balloons()
    # Тот самый пробел в заголовке
    st.header("🥳 Тренировка  🧠 Brain Gum 🧠  окончена!")
    
    percent = (st.session_state.score / total_count) * 100
    if percent == 100: 
        stars, rank = "⭐⭐⭐⭐⭐", "Легендарный результат! 🏆👑"
    elif percent >= 80: 
        stars, rank = "⭐⭐⭐⭐", "Почти идеал! 🥈🔥"
    elif percent >= 60: 
        stars, rank = "⭐⭐⭐", "Хорошая работа! 🥉💪"
    elif percent >= 40: 
        stars, rank = "⭐⭐", "Можно лучше! 🎖️🛠️"
    else: 
        stars, rank = "⭐", "Не сдавайся, попробуй еще раз! 🎒💡"

    st.write("")
    st.subheader(f"Твой рейтинг: {stars}")
    st.write(f"### {rank}")
    st.metric("Точных попаданий", f"{st.session_state.score} / {total_count}")
    
    if st.button("🚀 Начать новую серию"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
