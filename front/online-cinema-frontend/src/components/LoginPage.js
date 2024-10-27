import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { Link } from 'react-router-dom';
import * as Yup from 'yup';
import API_BASE_URL from '../config';
import './LoginPage.css';

const LoginSchema = Yup.object().shape({
  username_or_email: Yup.string().min(8, 'Минимум 8 символов').required('Обязательно для заполнения'),
  password: Yup.string().min(8, 'Минимум 8 символов').required('Обязательно для заполнения')
});

const LoginPage = () => {
  return (
    <div className="login-page">
      <h2>Вход</h2>
      <Formik
        initialValues={{ username_or_email: '', password: '' }}
        validationSchema={LoginSchema}
        onSubmit={(values, { setSubmitting }) => {
          setSubmitting(true);
          fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username_or_email: values.username_or_email,
              password: values.password
            })
          })
          .then(response => {
            if (!response.ok) throw new Error('Ошибка авторизации');
            return response.json();
          })
          .then(data => {
            localStorage.setItem('accessToken', data.accessToken);
            localStorage.setItem('refreshToken', data.refreshToken);
            setSubmitting(false);
            window.location.href = '/';
          })
          .catch(error => {
            console.error('Ошибка:', error);
            setSubmitting(false);
          });
        }}
      >
        {({ isSubmitting }) => (
          <Form className="login-form">
            <div className="form-group">
              <label htmlFor="username_or_email">Никнейм или Email:</label>
              <Field type="text" name="username_or_email" className="form-field" />
              <ErrorMessage name="username_or_email" component="div" className="error" />
            </div>
            <div className="form-group">
              <label htmlFor="password">Пароль:</label>
              <Field type="password" name="password" className="form-field" />
              <ErrorMessage name="password" component="div" className="error" />
            </div>
            <button type="submit" disabled={isSubmitting} className="login-button">
              Войти
            </button>
          </Form>
        )}
      </Formik>
      <p className="register-link">Нет аккаунта? <Link to="/register">Зарегистрироваться</Link></p>
    </div>
  );
};

export default LoginPage;
