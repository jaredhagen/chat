import { Col, Button, Form, Input, Row, Typography } from "antd";
import { Link, Redirect } from "react-router-dom";
import { useAuth, useRegisterUser } from "./hooks";

function LoginPage() {
  const auth = useAuth();
  const registerUser = useRegisterUser();

  const onFinish = (username) => {
    registerUser.mutate(username);
  };

  return registerUser.isSuccess ? (
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
            <Typography.Title>Sign up to Chat</Typography.Title>
          </Col>
        </Row>
        <Row>
          <Col offset={7} span={10}>
            <Form
              name="register"
              initialValues={{
                remember: true,
              }}
              onFinish={onFinish}
            >
              <Form.Item
                name="username"
                hasFeedback={registerUser.isLoading || registerUser.isError}
                validateStatus={
                  registerUser.isLoading
                    ? "validating"
                    : registerUser.isError
                    ? "error"
                    : ""
                }
                help={registerUser.isError ? "Username already taken" : null}
                rules={[
                  {
                    required: true,
                    message: "Please input a username",
                  },
                ]}
              >
                <Input placeholder="Username" />
              </Form.Item>
              <Form.Item>
                <Button block type="primary" htmlType="submit">
                  Sign up
                </Button>
              </Form.Item>
            </Form>
          </Col>
        </Row>
        <Row justify="center">
          <Col>
            <Link to="/login">Been here before? Click here to log in.</Link>
          </Col>
        </Row>
      </Col>
    </Row>
  );
}

export default LoginPage;
