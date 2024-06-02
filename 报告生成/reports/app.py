from flask import Flask, render_template, request, send_file, url_for, session, abort
from docx import Document
from werkzeug.utils import secure_filename
import os
from docx2pdf import convert
import pythoncom

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('report.html')

@app.route('/generate_report/<template_type>', methods=['POST'])
def generate_report(template_type):
    try:
        # 获取表单数据
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
        template_path = os.path.join(app.root_path, 'templates', f"{template_type}.docx")
        if not os.path.exists(template_path):
            abort(404, description="Template not found")
        
        document = Document(template_path)

        # 替换模板中的占位符
        placeholders = {
            '${试验名称}$': title,
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
        report_dir = os.path.join('报告生成','reports','generated_reports')  # 报告生成-reports 目录下的 generated_reports 文件夹
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        filename = secure_filename(f"{student_id}.docx")  # 先生成一个临时文件名
        report_path = os.path.join(report_dir, filename)
        document.save(report_path)

        # 生成最终的文件名
        final_filename = f"{title}_{name}_{student_id}_{template_type}.docx"
        final_report_path = os.path.join(report_dir, final_filename)
        os.rename(report_path, final_report_path)

        # 初始化COM库
        pythoncom.CoInitialize()

        try:
            # 生成 PDF 文件
            pdf_filename = f"{title}_{name}_{student_id}_{template_type}.pdf"
            pdf_path = os.path.join(report_dir, pdf_filename)
            convert(final_report_path, pdf_path)
        finally:
            # 取消初始化COM库
            pythoncom.CoUninitialize()

        # 将报告文件内容传递给预览页面
        return render_template('preview.html', name=name, student_id=student_id, template_type=template_type, pdf_filename=pdf_filename, title=title)
    except Exception as e:
        return f"出现错误：{str(e)}"

@app.route('/download_report/<title>_<name>_<student_id>_<template_type>.docx')
def download_report(title, name, student_id, template_type):
    try:
        filename = f"{title}_{name}_{student_id}_{template_type}.docx"
        report_path = os.path.join('generated_reports', filename)
        return send_file(report_path, as_attachment=True)
    except Exception as e:
        return f"出现错误：{str(e)}"

@app.route('/preview_pdf/<pdf_filename>')
def preview_pdf(pdf_filename):
    try:
        pdf_path = os.path.join('generated_reports', pdf_filename)
        return send_file(pdf_path)
    except Exception as e:
        return f"出现错误：{str(e)}"

@app.route('/modify_info', methods=['POST'])
def modify_info():
    name = request.form['name']
    student_id = request.form['student_id']
    template_type = request.form['template_type']
    title = request.form['title']
    return render_template('report.html', name=name, student_id=student_id, template_type=template_type, title=title)

if __name__ == '__main__':
    app.run(debug=True)
