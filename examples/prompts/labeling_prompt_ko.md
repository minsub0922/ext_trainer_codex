# 한국어 K/V 라벨링 프롬프트 예시

아래 문서를 읽고 지정된 스키마에 맞춰 JSON만 반환하세요.

- 누락된 값은 `null`로 유지합니다.
- 스키마에 없는 필드는 추가하지 않습니다.
- 값이 문서에 명시되어 있지 않으면 추정하지 않습니다.

출력 예시:

```json
{
  "invoice_id": null,
  "vendor_name": null,
  "total_amount": null,
  "issue_date": null
}
```
