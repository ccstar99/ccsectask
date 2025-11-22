from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from ccScoreSearch import GradeQuerySystem

app = Flask(__name__)
CORS(app)  # 允许跨域请求

system = GradeQuerySystem()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/student/<query>')
def get_student(query):
    try:
        result = system.query_student(query)
        if result:
            return jsonify({
                'success': True,
                'data': {
                    'student_id': result.student_id,
                    'student_name': result.student_name,
                    'exam_score': result.exam_score,
                    'homework_avg': result.homework_avg,
                    'homework_percent': result.homework_percent,
                    'exam_type': result.exam_type,
                    'weighted_score': result.weighted_score,
                    'weighted_grade': result.weighted_grade,
                    'exam_grade': result.exam_grade,
                    'analysis': result.analysis,
                    'improvement_scenarios': result.get_improvement_scenarios()
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'未找到学生信息: {query}'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/students')
def get_all_students():
    try:
        students = []
        for data in system.students_data:
            students.append({
                'student_id': data[0],
                'student_name': data[1]
            })
        return jsonify({
            'success': True,
            'data': students
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取学生列表失败: {str(e)}'
        }), 500

@app.route('/api/class_stats')
def get_class_stats():
    try:
        grade_distribution = {
            "A 🏆": 0, "B+ 🌟": 0, "B ✅": 0,
            "C+ 📈": 0, "C 📊": 0, "D 📚": 0, "F ⚠️": 0
        }
        total_students = 0
        total_score = 0

        for data in system.students_data:
            student_id, name, exam_score, homework_avg, exam_type = data
            if exam_type != "未考试":  # 排除未考试学生
                report = system.query_student(student_id)
                if report.weighted_grade in grade_distribution:
                    grade_distribution[report.weighted_grade] += 1
                total_students += 1
                total_score += report.weighted_score

        avg_score = total_score / total_students if total_students > 0 else 0

        return jsonify({
            'success': True,
            'data': {
                'average_score': round(avg_score, 2),
                'total_students': total_students,
                'grade_distribution': grade_distribution
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取班级统计失败: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'students_count': len(system.students_data)})

if __name__ == '__main__':
    print("🎓 审计2501班高数成绩查询系统启动中...")
    print(f"📊 共加载 {len(system.students_data)} 名学生数据")
    print("🌐 服务地址: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)