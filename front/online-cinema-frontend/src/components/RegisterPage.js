import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { Link } from 'react-router-dom';
import * as Yup from 'yup';
import API_BASE_URL from '../config';
import './RegisterPage.css';

const RegistrationSchema = Yup.object().shape({
  username: Yup.string().min(8, 'Минимум 8 символов').required('Обязательно для заполнения'),
  email: Yup.string().email('Некорректный email').required('Обязательно для заполнения'),
  password: Yup.string().min(8, 'Минимум 8 символов').required('Обязательно для заполнения'),
  first_name: Yup.string().required('Имя обязательно'),
  last_name: Yup.string().required('Фамилия обязательна'),
});

const RegisterPage = () => {
  return (
    <div className="register-page">
      <h2>Регистрация</h2>
      <Formik
        initialValues={{ username: '', email: '', password: '', first_name: '', last_name: '' }}
        validationSchema={RegistrationSchema}
        onSubmit={(values, { setSubmitting }) => {
          setSubmitting(true);
          fetch(`${API_BASE_URL}/auth/registration`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(values),
          })
          .then(response => {
            if (!response.ok) throw new Error('Ошибка регистрации');
            return response.json();
          })
          .then(data => {
            setSubmitting(false);
            window.location.href = '/login';
          })
          .catch(error => {
            console.error('Ошибка регистрации:', error);
            setSubmitting(false);
          });
        }}
      >
        {({ isSubmitting }) => (
          <Form className="register-form">
            <div className="form-group">
              <label htmlFor="username">Никнейм:</label>
              <Field type="text" name="username" className="form-field" />
              <ErrorMessage name="username" component="div" className="error" />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <Field type="email" name="email" className="form-field" />
              <ErrorMessage name="email" component="div" className="error" />
            </div>
            <div className="form-group">
              <label htmlFor="password">Пароль:</label>
              <Field type="password" name="password" className="form-field" />
              <ErrorMessage name="password" component="div" className="error" />
            </div>
            <div className="form-group">
              <label htmlFor="first_name">Имя:</label>
              <Field type="text" name="first_name" className="form-field" />
              <ErrorMessage name="first_name" component="div" className="error" />
            </div>
            <div className="form-group">
              <label htmlFor="last_name">Фамилия:</label>
              <Field type="text" name="last_name" className="form-field" />
              <ErrorMessage name="last_name" component="div" className="error" />
            </div>
            <button type="submit" disabled={isSubmitting} className="register-button">
              Зарегистрироваться
            </button>
          </Form>
        )}
      </Formik>
      <p className="login-link">Уже есть аккаунт? <Link to="/login">Войти</Link></p>
    </div>
  );
};

export default RegisterPage;
