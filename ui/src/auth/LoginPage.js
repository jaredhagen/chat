import { Col, Button, Form, Input, Row, Typography } from "antd";
import { Link, Redirect } from "react-router-dom";
import { useAuth, useLogInUser } from "./hooks";

function LoginPage() {
  const auth = useAuth();
  const logInUser = useLogInUser();

  const onFinish = (credentials) => {
    logInUser.mutate(credentials);
  };

  return logInUser.isSuccess ? (
    <Redirect push={true} to={{ pathname: "/" }}></Redirect>
  ) : (
    <Row
      align="middle"
      style={{
        height: "100vh",
      }}
    >
      <Col span={24}>
        <Row justify="center">
          <Col>
            <Typography.Title>Log in to Chat</Typography.Title>
          </Col>
        </Row>
        <Row justify="center">
          <Col span={8}>
            <Form
              name="login"
              initialValues={{
                remember: true,
              }}
              onFinish={onFinish}
            >
              <Form.Item
                name="username"
                hasFeedback={logInUser.isLoading || logInUser.isError}
                validateStatus={
                  logInUser.isLoading
                    ? "validating"
                    : logInUser.isError
                    ? "error"
                    : ""
                }
                help={logInUser.isError ? "Unrecognized username" : null}
                rules={[
                  {
                    required: true,
                    message: "Please input your username",
                  },
                ]}
              >
                <Input placeholder="Username" />
              </Form.Item>
              <Form.Item>
                <Button block type="primary" htmlType="submit">
                  Log In
                </Button>
              </Form.Item>
            </Form>
          </Col>
        </Row>
        <Row justify="center">
          <Col>
            <Link to="/signup">New Here? Click here to sign up.</Link>
          </Col>
        </Row>
      </Col>
    </Row>
  );
}

export default LoginPage;
