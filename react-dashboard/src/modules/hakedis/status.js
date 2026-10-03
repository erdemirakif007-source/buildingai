const META = {
  taslak:        { label: 'Taslak',          tone: 'neutral'  },
  onay_bekliyor: { label: 'Onay bekliyor',   tone: 'warning'  },
  onaylandi:     { label: 'Onaylandı',        tone: 'success'  },
  reddedildi:    { label: 'Geri gönderildi', tone: 'danger'   },
}

export function getMeta(durum) {
  return META[durum] ?? { label: durum, tone: 'neutral' }
}

export function allowedActions(durum, caps) {
  return {
    canSubmit:  durum === 'taslak'        && !!caps?.can_submit,
    canRetract: durum === 'onay_bekliyor' && !!caps?.can_submit,
    canDraft:   durum === 'reddedildi'    && !!caps?.can_submit,
    canApprove: durum === 'onay_bekliyor' && !!caps?.can_review,
    canReject:  durum === 'onay_bekliyor' && !!caps?.can_review,
    canCancel:  durum === 'taslak'        && !!caps?.can_submit,
    canPdf:     (durum === 'onay_bekliyor' || durum === 'onaylandi'),
  }
}
