frappe.ui.form.on("Ha Pos Invoice", {
    after_save: function(frm) {
        // Call backend function to generate JSON
        frappe.call({
            method: "posprinter.fetchprint.generate_invoice_json",  // update with your actual python file path
            args: {
                invoice_id: frm.doc.name
            },
            callback: function(r) {
                if (r.message) {
                    // Convert to Blob for download
                    let dataStr = r.message;
                    let blob = new Blob([dataStr], { type: "text/plain;charset=utf-8" });

                    // Create a download link
                    let link = document.createElement("a");
                    link.href = URL.createObjectURL(blob);
                    link.download = frm.doc.name + "_invoice.txt"; // filename
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);

                    frappe.msgprint("Invoice successfuly sent to print manager.");
                }
            }
        });
    }
});
frappe.ui.form.on("Quotation", {
    on_submit: function(frm) {
        // Call backend function to generate JSON
        frappe.call({
            method: "posprinter.fetchprint.generate_quotation_json",  // update with your actual python file path
            args: {
                quote_id: frm.doc.name
            },
            callback: function(r) {
                if (r.message) {
                    // Convert to Blob for download
                    let dataStr = r.message;
                    let blob = new Blob([dataStr], { type: "text/plain;charset=utf-8" });

                    // Create a download link
                    let link = document.createElement("a");
                    link.href = URL.createObjectURL(blob);
                    link.download = frm.doc.name + "_invoice.txt"; // filename
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);

                    frappe.msgprint("Quotation successfuly sent to print manager.");
                }
            }
        });
    }
});
