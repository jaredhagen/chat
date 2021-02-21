import { Button, Form, Input } from "antd";

export default function SimpleForm({
  buttonText,
  errorMessage,
  form,
  hasError,
  isLoading,
  name,
  onFinish,
  inputName,
  inputPlaceholder,
  inputValidationMessage,
}) {
  const [defaultForm] = Form.useForm();

  return (
    <Form form={form || defaultForm} name={name} onFinish={onFinish}>
      <Form.Item
        name={inputName}
        hasFeedback={isLoading || hasError}
        validateStatus={isLoading ? "validating" : hasError ? "error" : null}
        help={hasError ? errorMessage : null}
        rules={[
          {
            required: true,
            message: { inputValidationMessage },
          },
        ]}
      >
        <Input placeholder={inputPlaceholder} />
      </Form.Item>
      <Form.Item>
        <Button block type="primary" htmlType="submit">
          {buttonText}
        </Button>
      </Form.Item>
    </Form>
  );
}
