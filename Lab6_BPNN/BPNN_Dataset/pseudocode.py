for i in train_set:
	normalize

initialize eta, number_of_hidden, w_input_to_hidden, w_hidden_to_output
for i from 0 to iterations:
	initialize delta_input_to_hidden, delta_hidden_to_output
	for j in train_set.subset:
		h_hidden = sigmoid(j .* w_input_to_hidden)
		h_output = h_hidden .* w_hidden_to_output
		err_output = j.label - h_output
		err_hidden = mul(h_hidden, ones - h_hidden) .* w_hidden_to_output * err_output
		err_input[k] = j[k] * (err_hidden .* w_input_to_hidden[k])
		delta_input_to_hidden[j][k] = eta * err_input .* h_input
		delta_hidden_to_output = eta * err_hidden .* h_hidden
	w_input_to_hidden += delta_input_to_hidden
	w_hidden_to_output += delta_hidden_to_output

