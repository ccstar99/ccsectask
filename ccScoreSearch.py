# 审计2501班高数成绩查询系统 - 优化修复版
# 修复计算精度、完善分析逻辑、丰富提升建议、优化场景模拟
import os


class StudentGradeReport:
    """学生成绩报告类"""

    def __init__(self, student_id, student_name, exam_score, homework_avg, exam_type, exam_weight=0.6,
                 homework_weight=0.4):
        self.student_id = student_id
        self.student_name = student_name
        self.exam_score = exam_score
        self.homework_avg = homework_avg
        self.exam_type = exam_type
        self.exam_weight = exam_weight
        self.homework_weight = homework_weight

        # 计算得出的属性 - 修复计算精度
        self.homework_percent = round(self.homework_avg * 10, 2)
        self.weighted_score = self.calculate_weighted_score()
        self.weighted_grade = self.determine_grade(self.weighted_score)
        self.exam_grade = self.determine_grade(self.exam_score) if self.exam_score is not None else "未考试"
        self.analysis = self.generate_analysis()

    def calculate_weighted_score(self):
        """计算加权成绩 - 修复精度问题"""
        if self.exam_score is None:  # 未考试情况
            return round(self.homework_percent, 2)
        weighted = self.exam_score * self.exam_weight + self.homework_percent * self.homework_weight
        return round(weighted, 2)

    def determine_grade(self, score):
        """确定等级 - 确保一致性"""
        if score is None:
            return "未考试"
        if score >= 90:
            return "A 🏆"
        elif score >= 85:
            return "B+ 🌟"
        elif score >= 80:
            return "B ✅"
        elif score >= 75:
            return "C+ 📈"
        elif score >= 70:
            return "C 📊"
        elif score >= 60:
            return "D 📚"
        else:
            return "F ⚠️"

    def generate_analysis(self):
        """生成学习分析 - 完善边缘情况处理"""
        analysis = {}

        # 优势分析 - 扩展更多情况
        if self.homework_percent == 100:
            analysis['strength'] = "🎯 作业完成完美！继续保持"
        elif self.homework_percent >= 95:
            analysis['strength'] = "🎯 作业完成极其认真细致"
        elif self.homework_percent >= 85:
            analysis['strength'] = "📝 作业表现稳定良好"
        elif self.homework_percent >= 70:
            analysis['strength'] = "✏️ 作业完成态度端正"
        elif self.homework_percent > 0:
            analysis['strength'] = "📖 有提交作业记录"
        else:
            analysis['strength'] = "⏳ 需要开始提交作业"

        # 考试表现分析
        if self.exam_score is not None:
            if self.exam_score >= 95:
                analysis['exam_strength'] = "🎯 考试表现非常出色"
            elif self.exam_score >= 85:
                analysis['exam_strength'] = "📊 考试发挥稳定良好"
            elif self.exam_score >= 70:
                analysis['exam_strength'] = "📈 考试表现有进步空间"

        # 挑战分析 - 完善边缘情况
        if self.exam_score is None:
            analysis['challenge'] = "📅 需要参加考试获得完整评价"
        elif self.exam_score < 60:
            analysis['challenge'] = "📚 基础知识需要系统加强"
        elif self.exam_score < 70:
            analysis['challenge'] = "⏱️ 考试技巧和时间管理需要提升"
        elif self.homework_percent < 60:
            analysis['challenge'] = "💪 平时学习投入需要显著增加"
        elif self.homework_percent < 70:
            analysis['challenge'] = "📝 作业完成质量有待提高"

        # 特殊类型分析
        if self.homework_percent > (self.exam_score or 0) + 15:
            analysis['special_note'] = "📖 作业表现优秀但考试发挥需要提升"
        elif self.exam_score and (self.exam_score > self.homework_percent + 15):
            analysis['special_note'] = "🎯 考试能力强但平时作业需要更认真"
        elif self.exam_type == "补考":
            analysis['special_note'] = "🔄 已通过补考展示进步"
        elif self.exam_type == "未考试":
            analysis['special_note'] = "⏳ 等待参加考试获得完整评价"

        # 提升建议 - 丰富化处理
        suggestions = []

        # 针对优秀学生的建议
        if self.weighted_grade in ["A 🏆", "B+ 🌟"]:
            if self.exam_score and self.exam_score >= 95:
                suggestions.append("🌟 保持优秀表现，可以挑战更高难度")
            else:
                suggestions.append("📚 继续保持，争取更高分数")

        # 针对中等学生的建议
        elif self.weighted_grade in ["B ✅", "C+ 📈"]:
            suggestions.append("📈 稳步提升，关注薄弱环节")
            if self.homework_percent < 85:
                suggestions.append("📝 提高作业完成质量")

        # 针对需要提升学生的建议
        elif self.weighted_grade in ["C 📊", "D 📚"]:
            suggestions.append("📚 加强基础概念理解和练习")
            if self.exam_score and self.exam_score < 70:
                suggestions.append("⏰ 改善考试时间管理")

        # 针对困难学生的建议
        elif self.weighted_grade == "F ⚠️":
            suggestions.append("👨‍🏫 急需寻求教师一对一辅导")
            suggestions.append("📖 从基础概念开始系统学习")

        # 特殊情况建议
        if self.exam_type == "补考":
            suggestions.append("🔄 补考通过，继续保持学习状态")
        if self.exam_type == "未考试":
            suggestions.append("📝 请尽快安排参加考试")
        if self.homework_percent < 50:
            suggestions.append("💪 增加平时学习时间投入")
        if self.exam_score and self.exam_score > self.homework_percent + 10:
            suggestions.append("📝 将考试能力转化为平时表现")
        if self.homework_percent > (self.exam_score or 0) + 10:
            suggestions.append("🔄 将作业认真态度转化为考试表现")

        analysis['suggestions'] = suggestions
        return analysis

    def get_improvement_scenarios(self):
        """提供提升场景模拟 - 确保所有学生都有建议"""
        scenarios = []

        # 对于未考试学生
        if self.exam_score is None:
            scenarios.append("📈 如果考试获得60分 → 最终约72.0分 → C 📊")
            scenarios.append("📈 如果考试获得75分 → 最终约81.0分 → B ✅")
            scenarios.append("📈 如果考试获得85分 → 最终约87.0分 → B+ 🌟")
            return scenarios

        # 场景1: 考试提升5-10分（根据当前分数）
        if self.exam_score < 95:
            if self.exam_score < 60:
                exam_improve = 10  # 低分学生提升更多
            else:
                exam_improve = 5

            new_exam = self.exam_score + exam_improve
            new_weighted = new_exam * self.exam_weight + self.homework_percent * self.homework_weight
            new_grade = self.determine_grade(new_weighted)
            scenarios.append(f"📈 考试提升{exam_improve}分 → 最终{new_weighted:.1f}分 → {new_grade}")

        # 场景2: 作业提升到更高水平
        if self.homework_percent < 100:
            if self.homework_percent < 70:
                target_homework = 85  # 低作业分先提到良好
            else:
                target_homework = 100  # 良好作业提到满分

            new_weighted = self.exam_score * self.exam_weight + target_homework * self.homework_weight
            new_grade = self.determine_grade(new_weighted)
            scenarios.append(f"📝 作业提升到{target_homework}分 → 最终{new_weighted:.1f}分 → {new_grade}")

        # 场景3: 双提升（考试+作业）
        if self.exam_score < 95 and self.homework_percent < 100:
            exam_improve = 5 if self.exam_score >= 60 else 10
            homework_target = 100 if self.homework_percent >= 70 else 85

            new_exam = self.exam_score + exam_improve
            new_weighted = new_exam * self.exam_weight + homework_target * self.homework_weight
            new_grade = self.determine_grade(new_weighted)
            scenarios.append(f"🚀 考试+作业双提升 → 最终{new_weighted:.1f}分 → {new_grade}")

        # 确保至少有一个场景
        if not scenarios:
            scenarios.append("🎯 表现优秀！继续保持当前学习状态")

        return scenarios


class GradeQuerySystem:
    """成绩查询系统"""

    def __init__(self):
        self.students_data = self.load_students_data()

    def load_students_data(self):
        """加载学生数据（基于真实数据）"""
        students = [
            # 格式: (学号, 姓名, 期中成绩, 作业平均分, 考试类型)
            ("20251504421", "黄熙童", 97, 9.9385, "第一次考试"),
            ("20251504333", "李怡萱", 95, 9.9923, "第一次考试"),
            ("20251504383", "王思颖", 95, 9.9846, "补考"),
            ("20251504424", "陈凯琳", 95, 8.4538, "补考"),
            ("20251504444", "杨凯茹", 95, 9.8385, "第一次考试"),
            ("20251504361", "易可芸", 91, 0.7692, "第一次考试"),
            ("20251504408", "吴雯晶", 90, 9.9692, "补考"),
            ("20251504369", "唐思琪", 89, 9.1615, "补考"),
            ("20251504345", "林钰然", 88, 9.9769, "第一次考试"),
            ("20251504392", "林伊婷", 88, 8.4154, "补考"),
            ("20251504365", "李春梅", 88, 8.9077, "第一次考试"),
            ("20251504418", "江莹", 87, 9.9154, "第一次考试"),
            ("20251504313", "杨洋", 86, 9.9846, "第一次考试"),
            ("20251504341", "罗雅晴", 85, 9.9462, "第一次考试"),
            ("20251504376", "巫嘉怡", 85, 9.7538, "补考"),
            ("20251504310", "李婧", 82, 9.9846, "第一次考试"),
            ("20251504427", "韦炜", 82, 9.9308, "第一次考试"),
            ("20251504434", "包睿", 82, 7.6846, "第一次考试"),
            ("20251504387", "杨泽浩", 81, 9.9462, "第一次考试"),
            ("20251504346", "梁铠岚", 80, 3.6538, "第一次考试"),
            ("20251504443", "张澜舰", 79, 8.4154, "第一次考试"),
            ("20251504438", "冯梓瑄", 78, 8.2231, "补考"),
            ("20251504428", "高一茗", 77, 9.9769, "第一次考试"),
            ("20251504353", "金彦晞", 76, 9.9538, "第一次考试"),
            ("20251504366", "蔡晓钰", 76, 10.0000, "第一次考试"),
            ("20251504321", "蓝思颖", 75, 9.9538, "第一次考试"),
            ("20251504314", "徐铭秀", 74, 9.9846, "第一次考试"),
            ("20251504386", "罗嘉泓", 74, 8.3231, "第一次考试"),
            ("20251504336", "罗舒笑", 72, 9.9692, "第一次考试"),
            ("20251504320", "吴林泽", 71, 6.8000, "补考"),
            ("20251504405", "黄琪", 70, 6.7615, "补考"),
            ("20251504413", "阮雪莹", 68, 9.9692, "第一次考试"),
            ("20251504449", "聂诗轩", 68, 9.2231, "补考"),
            ("20251504308", "陈怡霏", 66, 9.9846, "第一次考试"),
            ("20251504398", "黄若熙", 66, 8.2846, "补考"),
            ("20251504401", "陈心悦", 64, 9.9462, "第一次考试"),
            ("20251504431", "曾颖", 59, 9.9846, "补考"),
            ("20251504312", "庄钰", 58, 9.8846, "补考"),
            ("20251504329", "范蕊菲", 58, 9.6231, "第一次考试"),
            ("20251504331", "程菲", 57, 9.0538, "第一次考试"),
            ("20251504356", "陈钰泉", 52, 0.0000, "补考"),
            ("20251504307", "马英杰", 50, 7.3923, "补考"),
            ("20251504306", "陈国铭", 46, 9.8615, "第一次考试"),
            ("20251504354", "余泓毅", 46, 0.0000, "补考"),
            ("20251504323", "李畅", 42, 9.9846, "第一次考试"),
            ("20251504410", "柳妍惠", 34, 6.1769, "补考"),
            ("20251504357", "黄乐怡", 5, 4.4462, "补考"),
            ("20241704698", "赵栩柔", None, 0.0000, "未考试")
        ]

        return students

    def query_student(self, query):
        """查询指定学号或姓名的学生成绩报告"""
        for data in self.students_data:
            if data[0] == query or data[1] == query:
                student_id, name, exam_score, homework_avg, exam_type = data
                report = StudentGradeReport(student_id, name, exam_score, homework_avg, exam_type)
                return report

        return None  # 未找到学生

    def format_report(self, report):
        """格式化成绩报告输出"""
        # 清屏并显示标题
        os.system('cls' if os.name == 'nt' else 'clear')

        output = []
        output.append("╔══════════════════════════════════════════════════╗")
        output.append("║              🎓 审计2501班高数成绩报告           ║")
        output.append("╚══════════════════════════════════════════════════╝")
        output.append("")

        # 学生基本信息
        output.append("╭────────────────── 学生信息 ──────────────────╮")
        output.append(f"│ 👤 学生姓名: {report.student_name:<30} │")
        output.append(f"│ 🆔 学号: {report.student_id:<34} │")
        output.append(f"│ 📋 考试情况: {report.exam_type:<32} │")
        output.append("╰──────────────────────────────────────────────╯")
        output.append("")

        # 成绩对比卡片
        output.append("╭───────────────── 成绩对比 ─────────────────╮")
        output.append("│                                              │")

        # 期中考试成绩卡片
        if report.exam_score is not None:
            output.append(f"│ 🎯 期中考试成绩: {report.exam_score:<5}分              │")
            output.append(f"│    等级: {report.exam_grade:<30} │")
        else:
            output.append(f"│ 🎯 期中考试成绩: 未参加考试              │")
            output.append(f"│    等级: {report.exam_grade:<30} │")

        output.append("│                                              │")

        # 加权综合成绩卡片
        output.append(f"│ 📈 综合成绩(加权): {report.weighted_score:<5}分            │")
        output.append(f"│    等级: {report.weighted_grade:<30} │")
        output.append("│                                              │")
        output.append(f"│ 💡 评分权重: 期中考试60% + 平时作业40%      │")
        output.append("│                                              │")
        output.append("╰──────────────────────────────────────────────╯")
        output.append("")

        # 成绩明细
        output.append("╭───────────────── 成绩明细 ─────────────────╮")
        output.append("│                                              │")
        output.append(
            f"│ • 期中考试: {report.exam_score if report.exam_score is not None else '未参加':<5}分 (权重60%)     │")
        output.append(f"│ • 平时作业: {report.homework_percent:<5.1f}分 (权重40%)                 │")
        output.append("│                                              │")
        output.append("╰──────────────────────────────────────────────╯")
        output.append("")

        # 学习分析
        output.append("╭───────────────── 学习分析 ─────────────────╮")
        output.append("│                                              │")
        if 'strength' in report.analysis:
            output.append(f"│ ✅ {report.analysis['strength']:<40} │")
        if 'exam_strength' in report.analysis:
            output.append(f"│ 🎯 {report.analysis['exam_strength']:<39} │")
        if 'challenge' in report.analysis:
            output.append(f"│ ⚠️  {report.analysis['challenge']:<39} │")
        if 'special_note' in report.analysis:
            output.append(f"│ 💡 {report.analysis['special_note']:<39} │")
        output.append("│                                              │")
        output.append("╰──────────────────────────────────────────────╯")
        output.append("")

        # 改进建议
        if report.analysis['suggestions']:
            output.append("╭───────────────── 改进建议 ─────────────────╮")
            output.append("│                                              │")
            for suggestion in report.analysis['suggestions']:
                output.append(f"│ {suggestion:<44} │")
            output.append("│                                              │")
            output.append("╰──────────────────────────────────────────────╯")
            output.append("")

        # 提升空间模拟
        scenarios = report.get_improvement_scenarios()
        if scenarios:
            output.append("╭───────────────── 提升空间 ─────────────────╮")
            output.append("│                                              │")
            for scenario in scenarios:
                output.append(f"│ {scenario:<44} │")
            output.append("│                                              │")
            output.append("╰──────────────────────────────────────────────╯")
            output.append("")

        return "\n".join(output)

    def list_all_students(self):
        """列出所有学生学号和姓名（用于参考）"""
        output = []
        output.append("╔══════════════════════════════════════════════════╗")
        output.append("║                  👥 所有学生列表                 ║")
        output.append("╚══════════════════════════════════════════════════╝")
        output.append("")
        for i, data in enumerate(self.students_data, 1):
            output.append(f" {i:2d}. {data[0]} - {data[1]}")
        return "\n".join(output)

    def get_class_statistics(self):
        """获取班级统计信息"""
        grade_distribution = {"A 🏆": 0, "B+ 🌟": 0, "B ✅": 0, "C+ 📈": 0, "C 📊": 0, "D 📚": 0, "F ⚠️": 0}
        total_students = 0
        total_score = 0

        for data in self.students_data:
            student_id, name, exam_score, homework_avg, exam_type = data
            if exam_type != "未考试":  # 排除未考试学生
                report = StudentGradeReport(student_id, name, exam_score, homework_avg, exam_type)
                grade_distribution[report.weighted_grade] += 1
                total_students += 1
                total_score += report.weighted_score

        avg_score = round(total_score / total_students, 2) if total_students > 0 else 0

        output = []
        output.append("╔══════════════════════════════════════════════════╗")
        output.append("║                 📈 班级成绩统计                 ║")
        output.append("╚══════════════════════════════════════════════════╝")
        output.append("")
        output.append(f" 📊 平均分: {avg_score:.2f}分")
        output.append(" 🎯 等级分布:")
        for grade, count in grade_distribution.items():
            percentage = (count / total_students) * 100 if total_students > 0 else 0
            output.append(f"    {grade}: {count}人 ({percentage:.1f}%)")

        return "\n".join(output)


def print_welcome():
    """打印欢迎界面"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔══════════════════════════════════════════════════╗")
    print("║            🎓 审计2501班高数成绩查询系统         ║")
    print("╚══════════════════════════════════════════════════╝")
    print("")
    print(" 💡 功能说明:")
    print("   • 输入学号或姓名查询个人成绩报告")
    print("   • 输入 'list' 查看所有学生列表")
    print("   • 输入 'stats' 查看班级统计")
    print("   • 输入 'exit' 退出系统")
    print("")


def main():
    """主函数 - 交互式查询系统"""
    system = GradeQuerySystem()

    while True:
        print_welcome()
        user_input = input(" 🔍 请输入学号/姓名或命令: ").strip()

        if user_input.lower() == 'exit':
            print("\n 👋 感谢使用成绩查询系统，再见！")
            break

        elif user_input.lower() == 'list':
            print("\n" + system.list_all_students())
            input("\n ↵ 按回车键继续...")

        elif user_input.lower() == 'stats':
            print("\n" + system.get_class_statistics())
            input("\n ↵ 按回车键继续...")

        else:
            # 查询学生
            result = system.query_student(user_input)
            if result:
                print("\n" + system.format_report(result))
                input("\n ↵ 按回车键返回主菜单...")
            else:
                print(f"\n ❌ 未找到 '{user_input}' 对应的学生信息")
                print(" 💡 提示: 输入 'list' 查看所有学生列表")
                input("\n ↵ 按回车键继续...")


# 运行主程序
if __name__ == "__main__":
    main()