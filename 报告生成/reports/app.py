from flask import Flask, render_template, request, send_file
from docx import Document
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('report.html')

@app.route('/generate_report/<template_type>', methods=['POST'])
def generate_report(template_type):
    try:
        title = request.form['title']
        name = request.form['name']
        student_id = request.form['student_id']
        major = request.form['major']
        advisor = request.form['advisor']
        contact = request.form['contact']
        purpose = request.form['purpose']
        principle = request.form['principle']
        design = request.form['design']
        steps = request.form['steps']
        phenomenon = request.form['phenomenon']
        data_processing = request.form['data_processing']
        conclusion = request.form['conclusion']
        discussion = request.form['discussion']

        # 读取选定的模板文件
        template_path = f"templates/{template_type}.docx"
        document = Document(template_path)

        # 替换模板中的占位符
        placeholders = {
            '${试验名称}$':title,
            '${姓名}$': name,
            '${学号}$': student_id,
            '${专业}$': major,
            '${指导教师}$': advisor,
            '${联系方式}$': contact,
            '${试验目的}$': purpose,
            '${试验原理}$': principle,
            '${试验设计}$': design,
            '${试验步骤}$': steps,
            '${试验现象}$': phenomenon,
            '${数据处理}$': data_processing,
            '${试验结论}$': conclusion,
            '${思考讨论}$': discussion
        }
        for paragraph in document.paragraphs:
            for old_text, new_text in placeholders.items():
                if old_text in paragraph.text:
                    paragraph.text = paragraph.text.replace(old_text, new_text)

        # 确保生成报告文件夹存在
        if not os.path.exists('generated_reports'):
            os.makedirs('generated_reports')

        # 保存生成的报告文件到 generated_reports 文件夹中
        filename = secure_filename(f"{name}_{student_id}_{template_type}.docx")
        report_path = os.path.join('generated_reports', filename)
        document.save(report_path)

        # 读取生成的报告文件内容
        report_content = read_document_content(report_path)

        # 将报告文件内容传递给预览页面
        return render_template('preview.html', name=name, student_id=student_id, template_type=template_type, report_content=report_content)
    except Exception as e:
        return f"出现错误：{str(e)}"

@app.route('/download_report/<name>_<student_id>_<template_type>.docx')
def download_report(name, student_id, template_type):
    try:
        filename = secure_filename(f"{name}_{student_id}_{template_type}.docx")
        report_path = os.path.join('generated_reports', filename)
        return send_file(report_path, as_attachment=True)
    except Exception as e:
        return f"出现错误：{str(e)}"

def read_document_content(path):
    document = Document(path)
    content = ""
    for paragraph in document.paragraphs:
        content += paragraph.text + "<br>"
    return content

@app.route('/modify_info', methods=['POST'])
def modify_info():
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)

